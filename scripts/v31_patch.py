from pathlib import Path
import re

hp=Path('app/src/main/assets/Ficha.html')
jp=Path('app/src/main/java/br/com/luan/fichalivre/MainActivity.java')
s=hp.read_text(encoding='utf-8')

# Version
s=s.replace('Versão instalada: <b>3.0</b> · nova base com assinatura definitiva','Versão instalada: <b>3.1</b> · passivos e testes múltiplos corrigidos')
s=s.replace("const APP_VERSION='3.0';","const APP_VERSION='3.1';")

# Passive points are independent from attribute/skill roll modifiers.
skills='''function renderSkills(){const c=char();let html='';for(const [a,list] of Object.entries(GROUPS))for(const sk of list){if(!c.skills[sk])continue;const rank=c.skills[sk],bonus=mod(c.attrs[a])+c.skillExtra,passive=Math.min(15,(c.passive[a]?10:0)+(rank==='M'?5:0)),rankText=rank==='T'?'Treinada · imune a desvantagem':rank==='M'?'Masterizada · imune a desvantagem · +5 passivo':'Normal';html+=`<div class="skill"><div><strong>${esc(sk)}</strong><small>${a} · ${rankText} · <span class="skill-passive">Passivo ${passive}/15</span></small></div><button data-skill="${sk}" data-group="${a}" title="Rolar 1d20${sign(bonus)}">d20 ${sign(bonus)}</button></div>`}$('#skills').className=html?'skillgrid':'';$('#skills').innerHTML=html||'<div class="empty">Sua ficha sem excesso de informação.<br>Escolha as perícias que deseja mostrar.</div>';$('#chooseSkills').textContent=html?'Editar perícias':'Escolher perícias'}'''
s,n=re.subn(r'function renderSkills\(\)\{.*?\}\nfor\(const f of fields\)',skills+'\nfor(const f of fields)',s,count=1,flags=re.S)
assert n==1

# Ascension wording: it grants 10 passive points, not a modifier-based passive score.
s=s.replace('Ascensão concluída · toque para desfazer com confirmação','Ascensão concluída · +10 passivo · toque para desfazer com confirmação')
s=s.replace("${asc?'Ascensão · DT 10':'Ascensão'}","${asc?'Ascensão · Passivo +10':'Ascensão'}")
s=s.replace('A DT passiva 10 será removida e o atributo voltará para 20.','Os 10 pontos passivos serão removidos e o atributo voltará para 20.')
s=s.replace('atributo restaurado para 20 e DT passiva removida.','atributo restaurado para 20 e +10 passivo removido.')
s=s.replace('voltou a 10 e recebeu DT passiva 10.','voltou a 10 e recebeu +10 passivo.')
s=s.replace('Use a estrela de Ascensão quando o atributo chegar a 20. A estrela fica dourada, o atributo volta a 10 e recebe DT passiva 10.','Use a estrela de Ascensão quando o atributo chegar a 20. A estrela fica dourada, o atributo volta a 10 e concede +10 pontos passivos às perícias ligadas a ele.')
s=s.replace('O passivo é 10 + os mesmos modificadores. Masterizada mantém a imunidade à desvantagem de Treinada e acrescenta +5 apenas ao passivo.','Pontos passivos não usam modificador do atributo nem ajuste manual. Ascensão concede +10; Masterizada concede +5; o máximo é 15. Masterizada mantém a imunidade à desvantagem de Treinada.')
s=s.replace('Masterizado é a evolução de Treinado: mantém a imunidade à desvantagem e acrescenta +5 ao valor passivo da perícia. Esse +5 não entra na rolagem.','Masterizado é a evolução de Treinado: mantém a imunidade à desvantagem e acrescenta +5 pontos passivos. Ascensão do atributo concede +10 pontos passivos. Máximo: 15. Nenhum desses pontos entra na rolagem.')

# Formula hint for multiple d20 checks.
s=s.replace('Ex.: 1d20+3 · 2d6+4 · 1d6+1d4','Ex.: 1d20+3 · 3d20+4 = 3 testes separados com +4 em cada · 2d6+4')

# Multiple d20 + flat modifier = separate tests. The flat modifier is applied to EACH d20.
# Other formulas preserve the classic summed-dice behavior.
roll='''function roll(input,label='Rolagem livre',switchToDice=true){try{const parsed=parseFormula(input);let total=0;const parts=[];const d20Terms=parsed.terms.filter(t=>t.n&&t.sides===20&&t.sign===1),otherDice=parsed.terms.filter(t=>t.n&&!(t.sides===20&&t.sign===1)),flatTerms=parsed.terms.filter(t=>!t.n);if(d20Terms.length===1&&d20Terms[0].n>1&&otherDice.length===0){const d=d20Terms[0],modifier=flatTerms.reduce((a,t)=>a+t.sign*t.value,0),raw=Array.from({length:d.n},()=>die(20)),tests=raw.map(v=>v+modifier);total=tests.reduce((a,b)=>a+b,0);for(let i=0;i<tests.length;i++)parts.push(`Teste ${i+1}: ${raw[i]}${modifier?sign(modifier):''} = ${tests[i]}`);parts.push(`Soma dos ${d.n} testes: ${total}`)}else{for(const t of parsed.terms){if(t.n){const values=Array.from({length:t.n},()=>die(t.sides));total+=t.sign*values.reduce((a,b)=>a+b,0);parts.push(`${t.sign<0?'−':'+'} ${t.n}d${t.sides} [${values.join(', ')}]`)}else{total+=t.sign*t.value;parts.push(`${t.sign<0?'−':'+'} ${t.value}`)}}}const detail=parts.join(' · ').replace(/^\\+ /,'');const entry={id:uid(),at:Date.now(),formula:parsed.formula,label,total,detail};char().history.unshift(entry);char().history=char().history.slice(0,100);$('#rollError').textContent='';$('#resultName').textContent=label+' · '+parsed.formula;$('#total').textContent=total;$('#breakdown').textContent=detail;renderHistory();$('#lastRoll').textContent=String(total);if(switchToDice)mobileView('dice');changed();return entry}catch(e){$('#rollError').textContent=e.message;return null}}'''
s,n=re.subn(r"function roll\(input,label='Rolagem livre',switchToDice=true\)\{.*?\}\n\$\('#rollForm'\)",roll+"\n$('#rollForm')",s,count=1,flags=re.S)
assert n==1

assert "const APP_VERSION='3.1'" in s
assert "passive=Math.min(15,(c.passive[a]?10:0)+(rank==='M'?5:0))" in s
assert '3d20+4 = 3 testes separados' in s
assert 'Soma dos ${d.n} testes' in s
hp.write_text(s,encoding='utf-8')

j=jp.read_text(encoding='utf-8').replace('@JavascriptInterface public String getAppVersion() { return "3.0"; }','@JavascriptInterface public String getAppVersion() { return "3.1"; }')
assert 'return "3.1"' in j
jp.write_text(j,encoding='utf-8')
