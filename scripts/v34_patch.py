from pathlib import Path
import re

hp=Path('app/src/main/assets/Ficha.html')
jp=Path('app/src/main/java/br/com/luan/fichalivre/MainActivity.java')
s=hp.read_text(encoding='utf-8')

s=s.replace('Versão instalada: <b>3.3</b> · resultados de combate mais limpos','Versão instalada: <b>3.4</b> · resultados detalhados em combate')
s=s.replace("const APP_VERSION='3.3';","const APP_VERSION='3.4';")

# Resultado compacto nos campos de combate: 19 (d=15+4).
s=s.replace('</style></head>', '.combat-inline-result{font-size:13px;line-height:1.25;white-space:normal;text-align:center;word-break:break-word;padding:5px 6px}@media(max-width:780px){.combat-inline-result{font-size:12px}}' + '</style></head>', 1)

roll=r'''function roll(input,label='Rolagem livre',switchToDice=true){try{const parsed=parseFormula(input);let total=0;const parts=[];let inlineDetail='',combatText='';const d20Terms=parsed.terms.filter(t=>t.n&&t.sides===20&&t.sign===1),otherDice=parsed.terms.filter(t=>t.n&&!(t.sides===20&&t.sign===1)),flatTerms=parsed.terms.filter(t=>!t.n);if(d20Terms.length===1&&d20Terms[0].n>1&&otherDice.length===0){const d=d20Terms[0],modifier=flatTerms.reduce((a,t)=>a+t.sign*t.value,0),raw=Array.from({length:d.n},()=>die(20)),tests=raw.map(v=>v+modifier);total=tests.reduce((a,b)=>a+b,0);for(let i=0;i<tests.length;i++)parts.push(`Teste ${i+1}: ${raw[i]}${modifier?sign(modifier):''} = ${tests[i]}`);parts.push(`Soma dos ${d.n} testes: ${total}`);combatText=`Σ${total} · `+tests.map((v,i)=>`${v} (d=${raw[i]}${modifier?sign(modifier):''})`).join(' · ')}else if(d20Terms.length===1&&d20Terms[0].n===1&&otherDice.length===0){const modifier=flatTerms.reduce((a,t)=>a+t.sign*t.value,0),raw=die(20);total=raw+modifier;inlineDetail=`d=${raw}${modifier?sign(modifier):''}`;combatText=`${total} (${inlineDetail})`;parts.push(`1d20 [${raw}]${modifier?' '+sign(modifier):''}`)}else{const compact=[];for(const t of parsed.terms){if(t.n){const values=Array.from({length:t.n},()=>die(t.sides));total+=t.sign*values.reduce((a,b)=>a+b,0);parts.push(`${t.sign<0?'−':'+'} ${t.n}d${t.sides} [${values.join(', ')}]`);for(const v of values)compact.push(`${t.sign<0?'-':'+'}${v}`)}else{total+=t.sign*t.value;parts.push(`${t.sign<0?'−':'+'} ${t.value}`);compact.push(`${t.sign<0?'-':'+'}${t.value}`)}}const expr=compact.join('').replace(/^\+/,'');combatText=`${total} (d=${expr})`}const detail=parts.join(' · ').replace(/^\+ /,'');const entry={id:uid(),at:Date.now(),formula:parsed.formula,label,total,detail,combatText};char().history.unshift(entry);char().history=char().history.slice(0,100);$('#rollError').textContent='';$('#resultName').textContent=label+' · '+parsed.formula;$('#total').innerHTML=inlineDetail?`${total} <span class="total-detail">(${inlineDetail})</span>`:String(total);$('#breakdown').textContent=detail;renderHistory();$('#lastRoll').textContent=String(total);if(switchToDice)mobileView('dice');changed();return entry}catch(e){$('#rollError').textContent=e.message;return null}}'''
s,n=re.subn(r"function roll\(input,label='Rolagem livre',switchToDice=true\)\{.*?\}\n\$\('#rollForm'\)",roll+"\n$('#rollForm')",s,count=1,flags=re.S)
assert n==1

old='<div class="combat-inline-result" aria-live="polite">${esc(r.lastRoll[f].total)}</div>'
new='<div class="combat-inline-result" aria-live="polite" title="${esc(r.lastRoll[f].detail||\'\')}">${esc(r.lastRoll[f].combatText||r.lastRoll[f].total)}</div>'
assert old in s
s=s.replace(old,new)

old_store='row.lastRoll[f]={total:entry.total,detail:entry.detail,at:entry.at,formula:entry.formula}'
new_store='row.lastRoll[f]={total:entry.total,detail:entry.detail,combatText:entry.combatText,at:entry.at,formula:entry.formula}'
assert old_store in s
s=s.replace(old_store,new_store)

assert "const APP_VERSION='3.4'" in s
assert 'combatText=`${total} (${inlineDetail})`' in s
assert 'combatText=`Σ${total} · `' in s
assert 'combatText:entry.combatText' in s
assert 'r.lastRoll[f].combatText||r.lastRoll[f].total' in s
hp.write_text(s,encoding='utf-8')

j=jp.read_text(encoding='utf-8').replace('@JavascriptInterface public String getAppVersion() { return "3.3"; }','@JavascriptInterface public String getAppVersion() { return "3.4"; }')
assert 'return "3.4"' in j
jp.write_text(j,encoding='utf-8')
