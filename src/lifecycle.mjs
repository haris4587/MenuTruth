export function classify(tx) {
  const names={0:'UNINITIALIZED',1:'PENDING',2:'PROPOSING',3:'COMMITTING',4:'REVEALING',5:'ACCEPTED',6:'UNDETERMINED',7:'FINALIZED',8:'CANCELED',9:'APPEAL_REVEALING',10:'APPEAL_COMMITTING',11:'READY_TO_FINALIZE',12:'VALIDATORS_TIMEOUT',13:'LEADER_TIMEOUT'};
  const status=String(tx?.statusName??names[tx?.status]??tx?.status??'UNKNOWN').toUpperCase();
  const receipts=tx?.consensus_data?.leader_receipt;
  const receipt=Array.isArray(receipts)?(receipts.find(r=>r.mode==='leader')??receipts[0]):receipts;
  const result=receipt?.execution_result??tx?.execution_result;
  if(['CANCELED','CANCELLED','UNDETERMINED','LEADER_TIMEOUT','VALIDATORS_TIMEOUT'].includes(status))return {phase:'failed',label:status};
  if(['ACCEPTED','FINALIZED'].includes(status)) {
    if(result!==undefined && !['SUCCESS',0,'0'].includes(result))return {phase:'failed',label:'Execution reverted'};
    return {phase:status==='FINALIZED'?'finalized':'accepted',label:status};
  }
  return {phase:'pending',label:status};
}
export const short=(s)=>s?`${s.slice(0,8)}…${s.slice(-6)}`:'Not deployed';
