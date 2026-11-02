import unittest, types, pathlib, json
from unittest.mock import Mock
source = pathlib.Path('contracts/menutruth.py').read_text().replace('from genlayer import *', '')
class Return:
    def __init__(self, calldata): self.calldata=calldata
class Store(dict): pass
sender='0x'+'1'*40
message=types.SimpleNamespace(sender_address=sender)
public=types.SimpleNamespace(write=lambda f:f, view=lambda f:f)
nondet=types.SimpleNamespace(exec_prompt=Mock())
def consensus(leader, validator):
    value=leader()
    if not validator(Return(value)): raise ValueError('Consensus rejected')
    return value
vm=types.SimpleNamespace(Return=Return, run_nondet_unsafe=consensus)
class Contract: pass
gl=types.SimpleNamespace(Contract=Contract, public=public, message=message, nondet=nondet, vm=vm)
ns={'gl':gl,'TreeMap':dict,'u256':int}
exec(compile(source,'menutruth.py','exec'),ns)
MenuTruth=ns['MenuTruth']
class ContractTests(unittest.TestCase):
    def setUp(self):
        message.sender_address=sender
        self.c=MenuTruth(); self.c.dishes=Store();self.c.changes=Store();self.c.chefs=Store()
        nondet.exec_prompt.reset_mock(side_effect=True)
    def dish(self): self.c.register_dish('Soup','Vegan tomato soup','Tomato, water, salt','No major allergens declared')
    def change(self):
        self.dish(); self.c.submit_change('1','Tomato, milk, salt','Milk supplier label: milk','Added milk')
    def answer(self,states=('ISSUE','ISSUE','ISSUE')):
        return json.dumps({'checks':[{'id':i,'status':s,'reason':'Declared milk conflicts with claim','quote':'milk'} for i,s in zip(ns['CHECKS'],states)]})
    def test_register_commitment(self):
        self.dish(); row=json.loads(self.c.get_dish('1')); h=row.pop('commitment'); self.assertEqual(ns['digest'](ns['canonical'](row)),h)
    def test_manager_only_registration(self):
        message.sender_address='0x'+'2'*40
        with self.assertRaisesRegex(ValueError,'Manager'):self.dish()
    def test_empty_and_oversize_input(self):
        for value in ['', ' '*4, 'x'*101]:
            with self.assertRaises(ValueError):self.c.register_dish(value,'m','r','d')
        self.assertEqual(self.c.dish_count,0)
    def test_chef_permissions_and_revocation(self):
        self.dish(); chef='0x'+'aA'*20; self.c.set_chef(chef,True); message.sender_address=chef
        self.c.submit_change('1','r','e','n'); message.sender_address=sender;self.c.set_chef(chef,False);message.sender_address=chef
        with self.assertRaisesRegex(ValueError,'staff'):self.c.submit_change('1','r','e','n')
    def test_invalid_address(self):
        with self.assertRaises(ValueError):self.c.set_chef('0x'+'z'*40,True)
    def test_unknown_dish(self):
        with self.assertRaisesRegex(ValueError,'Dish'):self.c.submit_change('99','r','e','n')
    def test_review_independent_consensus(self):
        self.change();nondet.exec_prompt.side_effect=[self.answer(),self.answer()];self.c.review_change('1')
        self.assertEqual(nondet.exec_prompt.call_count,2)
        self.assertEqual(json.loads(self.c.get_change('1'))['review']['verdict'],'ACTION_REQUIRED')
    def test_disagreement_preserves_submission(self):
        self.change();before=self.c.get_change('1');nondet.exec_prompt.side_effect=[self.answer(),self.answer(('UNKNOWN',)*3)]
        with self.assertRaisesRegex(ValueError,'Consensus'):self.c.review_change('1')
        self.assertEqual(self.c.get_change('1'),before)
    def test_no_double_review(self):
        self.change();nondet.exec_prompt.return_value=self.answer();self.c.review_change('1')
        with self.assertRaisesRegex(ValueError,'Already'):self.c.review_change('1')
    def test_acknowledgement_retains_verdict(self):
        self.change();nondet.exec_prompt.return_value=self.answer();self.c.review_change('1');self.c.acknowledge('1','Remove vegan claim; update disclosure')
        row=json.loads(self.c.get_change('1'));self.assertEqual(row['status'],'ACKNOWLEDGED');self.assertEqual(row['review']['verdict'],'ACTION_REQUIRED')
        with self.assertRaises(ValueError):self.c.acknowledge('1','again')
    def test_ack_requires_review(self):
        self.change()
        with self.assertRaisesRegex(ValueError,'Review required'):self.c.acknowledge('1','x')
    def test_unauthorized_review_and_ack(self):
        self.change();message.sender_address='0x'+'3'*40
        with self.assertRaises(ValueError):self.c.review_change('1')
        with self.assertRaises(ValueError):self.c.acknowledge('1','x')
    def test_safe_precedence(self):
        for states,expected in [(('CONSISTENT',)*3,'CONSISTENT'),(('UNKNOWN',)*3,'INCONCLUSIVE'),(('ISSUE','UNKNOWN','CONSISTENT'),'ACTION_REQUIRED')]:
            self.assertEqual(ns['parse_result'](self.answer(states),'milk')['verdict'],expected)
    def test_bad_model_schema(self):
        for raw in ['oops','{}','{"checks":[]}',self.answer().replace('ISSUE','SAFE'),self.answer().replace('description','bogus')]:
            with self.assertRaises(Exception):ns['parse_result'](raw,'milk')
    def test_quote_must_exist(self):
        with self.assertRaisesRegex(ValueError,'Ungrounded'):ns['parse_result'](self.answer(),'tomato')
    def test_consistent_requires_quote(self):
        with self.assertRaisesRegex(ValueError,'required'):ns['parse_result'](self.answer().replace('"quote": "milk"','"quote": ""'),'milk')
    def test_immutable_baseline(self):
        self.change();baseline=self.c.get_dish('1');nondet.exec_prompt.return_value=self.answer();self.c.review_change('1');self.assertEqual(self.c.get_dish('1'),baseline)
    def test_info(self):self.assertEqual(json.loads(self.c.get_info())['project'],'MenuTruth')
if __name__=='__main__':unittest.main()
