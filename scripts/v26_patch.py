from pathlib import Path

hp=Path('app/src/main/assets/Ficha.html')
jp=Path('app/src/main/java/br/com/luan/fichalivre/MainActivity.java')
s=hp.read_text(encoding='utf-8')

s=s.replace('Versão instalada: <b>2.5</b> · Ascensão e cálculos revisados','Versão instalada: <b>2.6</b> · Ascensão reversível com confirmação')
s=s.replace("const APP_VERSION='2.5';","const APP_VERSION='2.6';")
s=s.replace("title=\"${asc?'Ascensão concluída · DT passiva 10':'Ascensão: requer atributo 20'}\"","title=\"${asc?'Ascensão concluída · toque para desfazer com confirmação':'Ascensão: requer atributo 20'}\"")

old="""$('#attrs').addEventListener('click',e=>{const b=e.target.closest('[data-ascension]');if(!b)return;const a=b.dataset.ascension,c=char();if(c.passive[a]){toast(`${NAMES[a]} já realizou Ascensão.`);return}if(c.attrs[a]!==20){toast(`Ascensão de ${NAMES[a]} requer atributo 20.`);return}c.attrs[a]=10;c.passive[a]=true;renderAttrs();renderSkills();renderResources();changed();toast(`${NAMES[a]} realizou Ascensão: voltou a 10 e recebeu DT passiva 10.`)});"""
new="""$('#attrs').addEventListener('click',e=>{const b=e.target.closest('[data-ascension]');if(!b)return;const a=b.dataset.ascension,c=char();if(c.passive[a]){const ok=confirm(`Desfazer a Ascensão de ${NAMES[a]}?\\n\\nA DT passiva 10 será removida e o atributo voltará para 20.`);if(!ok)return;c.passive[a]=false;c.attrs[a]=20;renderAttrs();renderSkills();renderResources();changed();toast(`Ascensão de ${NAMES[a]} desfeita: atributo restaurado para 20 e DT passiva removida.`);return}if(c.attrs[a]!==20){toast(`Ascensão de ${NAMES[a]} requer atributo 20.`);return}c.attrs[a]=10;c.passive[a]=true;renderAttrs();renderSkills();renderResources();changed();toast(`${NAMES[a]} realizou Ascensão: voltou a 10 e recebeu DT passiva 10.`)});"""
assert old in s
s=s.replace(old,new,1)

assert "const APP_VERSION='2.6'" in s
assert 'Desfazer a Ascensão de' in s
assert 'c.passive[a]=false;c.attrs[a]=20' in s
hp.write_text(s,encoding='utf-8')

j=jp.read_text(encoding='utf-8').replace('@JavascriptInterface public String getAppVersion() { return "2.5"; }','@JavascriptInterface public String getAppVersion() { return "2.6"; }')
assert 'return "2.6"' in j
jp.write_text(j,encoding='utf-8')
