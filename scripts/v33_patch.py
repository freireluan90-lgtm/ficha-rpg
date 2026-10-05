from pathlib import Path

hp=Path('app/src/main/assets/Ficha.html')
jp=Path('app/src/main/java/br/com/luan/fichalivre/MainActivity.java')
s=hp.read_text(encoding='utf-8')

s=s.replace('Versão instalada: <b>3.2</b> · resultado de perícia mais compacto','Versão instalada: <b>3.3</b> · resultados de combate mais limpos')
s=s.replace("const APP_VERSION='3.2';","const APP_VERSION='3.3';")

old='<div class="combat-inline-result" aria-live="polite"><small>Resultado</small>${esc(r.lastRoll[f].total)}</div>'
new='<div class="combat-inline-result" aria-live="polite">${esc(r.lastRoll[f].total)}</div>'
assert old in s
s=s.replace(old,new)

assert "const APP_VERSION='3.3'" in s
assert '<small>Resultado</small>${esc(r.lastRoll[f].total)}' not in s
assert '<div class="combat-inline-result" aria-live="polite">${esc(r.lastRoll[f].total)}</div>' in s
hp.write_text(s,encoding='utf-8')

j=jp.read_text(encoding='utf-8').replace('@JavascriptInterface public String getAppVersion() { return "3.2"; }','@JavascriptInterface public String getAppVersion() { return "3.3"; }')
assert 'return "3.3"' in j
jp.write_text(j,encoding='utf-8')
