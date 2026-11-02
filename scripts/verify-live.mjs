import {createClient} from 'genlayer-js';import {studionet} from 'genlayer-js/chains';import fs from 'node:fs';import assert from 'node:assert/strict';import {createHash} from 'node:crypto';import {classify} from '../src/lifecycle.mjs';
const cfg=JSON.parse(fs.readFileSync('dist/deployment.json'));const client=createClient({chain:studionet});
const read=async(name,args=[])=>JSON.parse(await client.readContract({address:cfg.address,functionName:name,args}));
const info=await read('get_info');assert.equal(info.project,'MenuTruth');assert.equal(info.owner,cfg.info.owner);
const dish=await read('get_dish',['1']),change=await read('get_change',['1']);
assert.equal(change.status,'ACKNOWLEDGED');assert.equal(change.review.verdict,'ACTION_REQUIRED');assert.ok(change.review.checks.every(c=>c.status==='ISSUE'));
const source=fs.readFileSync('contracts/menutruth.py','utf8');
const onchainSource=await client.getContractCode(cfg.address);assert.equal(onchainSource.trim(),source.trim(),'Live source must match repository');
const schema=await client.getContractSchema(cfg.address);assert.ok(schema,'Deployed schema must load');
const report={checkedAt:new Date().toISOString(),network:'Studionet',chainId:61999,address:cfg.address,sourceSha256:createHash('sha256').update(source).digest('hex'),liveSourceMatches:true,info,dish,change,transactions:[]};
for(const [name,hash] of Object.entries({deployment:cfg.deploymentHash,register_dish:'0xb1d501c3c8571fd5b734b95930e63f5798a97006a7c3aed648ef6001fd597621',submit_change:'0xfe1055971818aa15670552b970832029665dd59fb78fe8e35b20759bd24600e4',staff_case_fix:'0x3eda40e9676516297c2e524fd4edb05d02c2b32ef3a4aaec5b351de69e5fa146',review_change:'0x28c8ec7e5db636359f7c5a77c0c7c42359544b89b00d55ca052414f16c2fd9ed',acknowledge:'0x0fbfada543730a9f6c29458d9317c72cec1cb596548cee4f66940bc01e90f27e'})){
 const tx=await client.getTransaction({hash});const state=classify(tx);assert.equal(state.phase,'finalized',name+' must finalize successfully');
 const receipts=tx.consensus_data?.leader_receipt||[];if(name!=='staff_case_fix')assert.ok(receipts.length&&(receipts.find(r=>r.mode==='leader')??receipts[0]).execution_result==='SUCCESS',name+' execution');
 const compact={name,hash,status:tx.statusName,execution:receipts.map(r=>r.execution_result),note:name==='staff_case_fix'?'Studio sandbox upgrade has no leader receipt; live source equality verified separately':undefined,votes:tx.consensus_data?.votes,url:'https://explorer-studio.genlayer.com/tx/'+hash};report.transactions.push(compact);
}
fs.writeFileSync('evidence/live-verification.json',JSON.stringify(report,null,2));console.log(JSON.stringify({verified:true,transactions:report.transactions.length,verdict:change.review.verdict}));
