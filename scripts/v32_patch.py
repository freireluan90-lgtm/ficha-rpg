from pathlib import Path
import re

hp=Path('app/src/main/assets/Ficha.html')
jp=Path('app/src/main/java/br/com/luan/fichalivre/MainActivity.java')
s=hp.read_text(encoding='utf-8')

# Version
s=s.replace('Versão instalada: <b>3.1</b> · passivos e testes múltiplos corrigidos','Versão instalada: <b>3.2</b> · resultado de perícia mais compacto')
s=s.replace("const APP_VERSION='3.1';","const APP_VERSION='3.2';")

# Remove the redundant "Resultado" eyebrow above the dice result, when present.
s=re.sub(r'<div class="eyebrow">\s*Resultado(?: da rolagem)?\s*</div>','',s,count=1,flags=re.I)

# Compact inline detail beside the total, e.g. 16 (d=13+3).
css='.total-detail{display:inline-block;font:600 18px/1.2 Consolas,monospace;color:var(--muted);white-space:nowrap;vertical-align:middle;margin-left:8px}.dicecard .total .total-detail{font-size:18px}@media(max-width:780px){.dicecard .total .total-detail{font-size:14px;margin-left:5px}}'
s=s.replace('</style></head>',css+'</style></head>',1)

roll='''function roll(input,label='Rolagem livre',switchToDice=true){try{const parsed=parseFormula(input);let total=0;const parts=[];let inlineDetail='';const d20Terms=parsed.terms.filter(t=>t.n&&t.sides===20&&t.sign===1),otherDice=parsed.terms.filter(t=>t.n&&!(t.sides===20&&t.sign===1)),flatTerms=parsed.terms.filter(t=>!t.n);if(d20Terms.length===1&&d20Terms[0].n>1&&otherDice.length===0){const d=d20Terms[0],modifier=flatTerms.reduce((a,t)=>a+t.sign*t.value,0),raw=Array.from({length:d.n},()=>die(20)),tests=raw.map(v=>v+modifier);total=tests.reduce((a,b)=>a+b,0);for(let i=0;i<tests.length;i++)parts.push(`Teste ${i+1}: ${raw[i]}${modifier?sign(modifier):''} = ${tests[i]}`);parts.push(`Soma dos ${d.n} testes: ${total}`)}else if(d20Terms.length===1&&d20Terms[0].n===1&&otherDice.length===0){const modifier=flatTerms.reduce((a,t)=>a+t.sign*t.value,0),raw=die(20);total=raw+modifier;inlineDetail=`d=${raw}${modifier?sign(modifier):''}`;parts.push(`1d20 [${raw}]${modifier?' '+sign(modifier):''}`)}else{for(const t of parsed.terms){if(t.n){const values=Array.from({length:t.n},()=>die(t.sides));total+=t.sign*values.reduce((a,b)=>a+b,0);parts.push(`${t.sign<0?'−':'+'} ${t.n}d${t.sides} [${values.join(', ')}]`)}else{total+=t.sign*t.value;parts.push(`${t.sign<0?'−':'+'} ${t.value}`)}}}const detail=parts.join(' · ').replace(/^\\+ /,'');const entry={id:uid(),at:Date.now(),formula:parsed.formula,label,total,detail};char().history.unshift(entry);char().history=char().history.slice(0,100);$('#rollError').textContent='';$('#resultName').textContent=label+' · '+parsed.formula;$('#total').innerHTML=inlineDetail?`${total} <span class="total-detail">(${inlineDetail})</span>`:String(total);$('#breakdown').textContent=detail;renderHistory();$('#lastRoll').textContent=String(total);if(switchToDice)mobileView('dice');changed();return entry}catch(e){$('#rollError').textContent=e.message;return null}}'''
s,n=re.subn(r"function roll\(input,label='Rolagem livre',switchToDice=true\)\{.*?\}\n\$\('#rollForm'\)",roll+"\n$('#rollForm')",s,count=1,flags=re.S)
assert n==1

assert "const APP_VERSION='3.2'" in s
assert 'class="total-detail"' in s
assert 'inlineDetail=`d=${raw}${modifier?sign(modifier):\'\'}`' in s
assert 'Soma dos ${d.n} testes' in s
hp.write_text(s,encoding='utf-8')

j=jp.read_text(encoding='utf-8').replace('@JavascriptInterface public String getAppVersion() { return "3.1"; }','@JavascriptInterface public String getAppVersion() { return "3.2"; }')
assert 'return "3.2"' in j
jp.write_text(j,encoding='utf-8')
