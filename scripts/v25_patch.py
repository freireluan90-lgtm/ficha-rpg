from pathlib import Path
import re

hp=Path('app/src/main/assets/Ficha.html')
jp=Path('app/src/main/java/br/com/luan/fichalivre/MainActivity.java')
s=hp.read_text(encoding='utf-8')

s=s.replace('Versão instalada: <b>2.4</b> · atualizador nativo corrigido','Versão instalada: <b>2.5</b> · Ascensão e cálculos revisados').replace("const APP_VERSION='2.4';","const APP_VERSION='2.5';")
s=s.replace("const CLASSES={Colosso:'PV base: 12 + FIS · PE base: 6 + INT · +2 redução de dano · +1 C.A.',Combatente:'PV base: 10 + FIS · PE base: 8 + INT · +2 dano base · +2 C.A.',Especialista:'PV base: 9 + FIS · PE base: 9 + INT · +1 perícia · +2 MS',Irregular:'18 pontos para PV/PE + FIS/INT · Pode começar com um poder diferenciado, conforme o mestre.'};","const CLASSES={Colosso:'PV base: 12 + mod. FIS · PE base: 6 + mod. INT · +2 redução de dano · +1 C.A.',Combatente:'PV base: 10 + mod. FIS · PE base: 8 + mod. INT · +2 dano base · +2 C.A.',Especialista:'PV base: 9 + mod. FIS · PE base: 9 + mod. INT · +1 perícia · +2 MS',Irregular:'18 pontos para PV/PE + mod. FIS/INT · Pode começar com um poder diferenciado, conforme o mestre.'};")

css='''.ascension-star{width:34px;height:34px;padding:0;margin:8px auto 0;display:grid;place-items:center;border:0;background:transparent!important;font-size:27px;line-height:1;color:color-mix(in srgb,var(--sheet-ink) 58%,transparent)}.ascension-star:hover{color:#d4a514;transform:scale(1.06)}.ascension-star.done{color:#e2b51f;text-shadow:0 1px 0 #8a6510,0 0 9px #f5c92855}.ascension-caption{font-size:9px;color:var(--muted);margin-top:1px}.skill-passive{font-weight:700;color:var(--sheet-accent)}'''
s=s.replace('</style></head>',css+'</style></head>',1)

attrs='''function renderAttrs(){const c=char();$('#attrs').innerHTML=Object.keys(GROUPS).map(a=>{const asc=!!c.passive[a];return `<div class="attr"><div class="tag">${a}</div><input type="number" min="1" max="20" value="${c.attrs[a]}" data-attr="${a}" aria-label="${NAMES[a]}"><div class="mod" id="mod-${a}">${sign(mod(c.attrs[a]))}</div><button type="button" class="ascension-star ${asc?'done':''}" data-ascension="${a}" title="${asc?'Ascensão concluída · DT passiva 10':'Ascensão: requer atributo 20'}">${asc?'★':'☆'}</button><div class="ascension-caption">${asc?'Ascensão · DT 10':'Ascensão'}</div></div>`}).join('');renderBudget()}
function renderBudget(){const c=char(),sum=Object.values(c.attrs).reduce((a,b)=>a+b,0),r=60-sum,asc=Object.values(c.passive||{}).filter(Boolean).length;$('#budget').classList.toggle('bad',r<0);$('#budget').textContent=asc?`${sum} pontos atuais · Ascensões: ${asc}`:`${sum} / 60 pontos · ${r>=0?r+' livres':-r+' acima da base inicial'}`}'''
s,n=re.subn(r'function renderAttrs\(\)\{.*?\nfunction renderResources',attrs+'\nfunction renderResources',s,count=1,flags=re.S)
assert n==1

skills='''function renderSkills(){const c=char();let html='';for(const [a,list] of Object.entries(GROUPS))for(const sk of list){if(!c.skills[sk])continue;const rank=c.skills[sk],bonus=mod(c.attrs[a])+c.skillExtra,passive=10+bonus+(rank==='M'?5:0),rankText=rank==='T'?'Treinada · imune a desvantagem':rank==='M'?'Masterizada · imune a desvantagem · +5 passivo':'Normal';html+=`<div class="skill"><div><strong>${esc(sk)}</strong><small>${a} · ${rankText} · <span class="skill-passive">Passivo ${passive}</span></small></div><button data-skill="${sk}" data-group="${a}" title="Rolar 1d20${sign(bonus)}">d20 ${sign(bonus)}</button></div>`}$('#skills').className=html?'skillgrid':'';$('#skills').innerHTML=html||'<div class="empty">Sua ficha sem excesso de informação.<br>Escolha as perícias que deseja mostrar.</div>';$('#chooseSkills').textContent=html?'Editar perícias':'Escolher perícias'}'''
s,n=re.subn(r'function renderSkills\(\)\{.*?\}\nfor\(const f of fields\)',skills+'\nfor(const f of fields)',s,count=1,flags=re.S)
assert n==1

s=s.replace("if(e.target.dataset.passive){char().passive[e.target.dataset.passive]=e.target.checked;changed()}","")
needle="$('#attrs').addEventListener('focusout',e=>{if(e.target.dataset.attr){e.target.value=char().attrs[e.target.dataset.attr];e.target.setCustomValidity('')}});"
asc="""$('#attrs').addEventListener('click',e=>{const b=e.target.closest('[data-ascension]');if(!b)return;const a=b.dataset.ascension,c=char();if(c.passive[a]){toast(`${NAMES[a]} já realizou Ascensão.`);return}if(c.attrs[a]!==20){toast(`Ascensão de ${NAMES[a]} requer atributo 20.`);return}c.attrs[a]=10;c.passive[a]=true;renderAttrs();renderSkills();renderResources();changed();toast(`${NAMES[a]} realizou Ascensão: voltou a 10 e recebeu DT passiva 10.`)});"""
assert needle in s
s=s.replace(needle,needle+asc,1)
s=s.replace("['M','Masterizada (M)']","['M','Masterizada (M) · inclui Treinada']")

repls={
'Marque DT passiva 10 após converter um atributo de 20 para 10. A alteração do valor é manual. O saldo mostra apenas a soma atual, sem reconstruir pontos de conversões ou evoluções.':'Use a estrela de Ascensão quando o atributo chegar a 20. A estrela fica dourada, o atributo volta a 10 e recebe DT passiva 10.',
'Teste: 1d20 + modificador do atributo + ajuste manual. Masterização acrescenta +5 apenas ao modificador passivo, não à rolagem.':'Teste: 1d20 + modificador do atributo + ajuste manual. O passivo é 10 + os mesmos modificadores. Masterizada mantém a imunidade à desvantagem de Treinada e acrescenta +5 apenas ao passivo.',
'Treinado: imunidade a desvantagem. Masterizado: +5 no modificador passivo. A relação entre treino e masterização ainda não foi definida, por isso a ficha não acrescenta imunidade automaticamente ao masterizado.':'Treinado: imunidade a desvantagem. Masterizado é a evolução de Treinado: mantém a imunidade à desvantagem e acrescenta +5 ao valor passivo da perícia. Esse +5 não entra na rolagem.',
'PV/PE máximos, C.A. e MS são calculados automaticamente por atributos, classe, nível e progressão.':'PV/PE máximos usam os modificadores de FIS/INT; C.A. usa 10 + modificador de DES + bônus de classe; MS usa 8 + modificador de DES + bônus de classe. Todos são recalculados automaticamente.'
}
for a,b in repls.items(): s=s.replace(a,b)

old="c.hpMax=hb+fis+(L-1)*c.hpGain;c.epMax=eb+intel+(L-1)*c.epGain;const bonus=c.class==='Combatente'?2:c.class==='Colosso'?1:0;c.ca=Math.min(c.class==='Combatente'?17:15,10+mod(des)+bonus);c.ms=8+mod(des)+(c.class==='Especialista'?2:0)"
new="c.hpMax=Math.max(0,hb+mod(fis)+(L-1)*c.hpGain);c.epMax=Math.max(0,eb+mod(intel)+(L-1)*c.epGain);const bonus=c.class==='Combatente'?2:c.class==='Colosso'?1:0;c.ca=10+mod(des)+bonus;c.ms=Math.max(0,8+mod(des)+(c.class==='Especialista'?2:0))"
assert old in s
s=s.replace(old,new,1)
s=s.replace("$('#classInfo').textContent=CLASSES[c.class]+' PV/PE máximos, C.A. e MS são automáticos.'","$('#classInfo').textContent=CLASSES[c.class]+' PV/PE máximos, C.A. e MS são automáticos quando aplicável; os demais bônus continuam na descrição.'")

assert "const APP_VERSION='2.5'" in s and 'data-ascension' in s and 'hb+mod(fis)' in s and 'Masterizada · imune a desvantagem' in s
hp.write_text(s,encoding='utf-8')

j=jp.read_text(encoding='utf-8').replace('@JavascriptInterface public String getAppVersion() { return "2.4"; }','@JavascriptInterface public String getAppVersion() { return "2.5"; }')
assert 'return "2.5"' in j
jp.write_text(j,encoding='utf-8')
