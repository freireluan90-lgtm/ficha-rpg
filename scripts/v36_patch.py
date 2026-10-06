from pathlib import Path
import re

hp=Path('app/src/main/assets/Ficha.html')
jp=Path('app/src/main/java/br/com/luan/fichalivre/MainActivity.java')
s=hp.read_text(encoding='utf-8')

s=s.replace('Versão instalada: <b>3.5</b> · novo ícone do aplicativo',
            'Versão instalada: <b>3.6</b> · resultado direto também nas perícias')
s=s.replace("const APP_VERSION='3.5';","const APP_VERSION='3.6';")

# Persist the last visible result for each skill.
s=s.replace("skillExtra:0,skills:{},abilities:", "skillExtra:0,skills:{},skillLastRoll:{},abilities:")
s=s.replace("if(typeof c.abilities!=='string')c.abilities='';",
            "if(!c.skillLastRoll||typeof c.skillLastRoll!=='object'||Array.isArray(c.skillLastRoll))c.skillLastRoll={};if(typeof c.abilities!=='string')c.abilities='';")

css='.skill-roll-wrap{display:flex;flex-direction:column;gap:4px;align-items:stretch;min-width:100px}.skill-inline-result{display:flex;align-items:center;justify-content:center;min-height:28px;padding:5px 6px;border-radius:8px;background:var(--sheet-accent);color:var(--sheet-color);font:800 13px/1.25 Consolas,monospace;text-align:center;word-break:break-word;box-shadow:0 2px 8px #0002}@media(max-width:780px){.skill-roll-wrap{min-width:92px}.skill-inline-result{font-size:12px}}'
s=s.replace('</style></head>',css+'</style></head>',1)

skills='''function renderSkills(){const c=char();c.skillLastRoll=c.skillLastRoll||{};let html='';for(const [a,list] of Object.entries(GROUPS))for(const sk of list){if(!c.skills[sk])continue;const rank=c.skills[sk],bonus=mod(c.attrs[a])+c.skillExtra,passive=Math.min(15,(c.passive[a]?10:0)+(rank==='M'?5:0)),rankText=rank==='T'?'Treinada · imune a desvantagem':rank==='M'?'Masterizada · imune a desvantagem · +5 passivo':'Normal',last=c.skillLastRoll[sk];html+=`<div class="skill"><div><strong>${esc(sk)}</strong><small>${a} · ${rankText} · <span class="skill-passive">Passivo ${passive}/15</span></small></div><div class="skill-roll-wrap">${last?`<div class="skill-inline-result" aria-live="polite" title="${esc(last.detail||'')}">${esc(last.combatText||last.total)}</div>`:''}<button data-skill="${sk}" data-group="${a}" title="Rolar 1d20${sign(bonus)}">d20 ${sign(bonus)}</button></div></div>`}$('#skills').className=html?'skillgrid':'';$('#skills').innerHTML=html||'<div class="empty">Sua ficha sem excesso de informação.<br>Escolha as perícias que deseja mostrar.</div>';$('#chooseSkills').textContent=html?'Editar perícias':'Escolher perícias'}'''
s,n=re.subn(r'function renderSkills\(\)\{.*?\}\nfor\(const f of fields\)',skills+'\nfor(const f of fields)',s,count=1,flags=re.S)
assert n==1

old="$('#skills').onclick=e=>{const b=e.target.closest('[data-skill]');if(b){const c=char(),bonus=mod(c.attrs[b.dataset.group])+c.skillExtra;const formula='1d20'+(bonus?sign(bonus):'');$('#formula').value=formula;roll(formula,b.dataset.skill)}};"
new="$('#skills').onclick=e=>{const b=e.target.closest('[data-skill]');if(b){const c=char(),bonus=mod(c.attrs[b.dataset.group])+c.skillExtra,formula='1d20'+(bonus?sign(bonus):'');$('#formula').value=formula;const entry=roll(formula,b.dataset.skill,false);if(entry){c.skillLastRoll=c.skillLastRoll||{};c.skillLastRoll[b.dataset.skill]={total:entry.total,detail:entry.detail,combatText:entry.combatText,at:entry.at,formula:entry.formula};renderSkills();changed()}}};"
assert old in s
s=s.replace(old,new)

assert "const APP_VERSION='3.6'" in s
assert 'skillLastRoll:{}' in s
assert 'class="skill-inline-result"' in s
assert "roll(formula,b.dataset.skill,false)" in s
hp.write_text(s,encoding='utf-8')

j=jp.read_text(encoding='utf-8').replace(
    '@JavascriptInterface public String getAppVersion() { return "3.5"; }',
    '@JavascriptInterface public String getAppVersion() { return "3.6"; }'
)
assert 'return "3.6"' in j
jp.write_text(j,encoding='utf-8')
