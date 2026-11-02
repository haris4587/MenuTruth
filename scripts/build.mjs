import {build} from 'esbuild';
await build({entryPoints:['src/app.mjs'],outfile:'dist/app.js',bundle:true,minify:true,format:'esm',target:['es2022']});
console.log('MenuTruth static bundle built');
