from pathlib import Path

hp=Path('app/src/main/assets/Ficha.html')
jp=Path('app/src/main/java/br/com/luan/fichalivre/MainActivity.java')

s=hp.read_text(encoding='utf-8')
s=s.replace('Versão instalada: <b>3.4</b> · resultados detalhados em combate',
            'Versão instalada: <b>3.5</b> · novo ícone do aplicativo')
s=s.replace("const APP_VERSION='3.4';","const APP_VERSION='3.5';")
assert "const APP_VERSION='3.5'" in s
hp.write_text(s,encoding='utf-8')

j=jp.read_text(encoding='utf-8').replace(
    '@JavascriptInterface public String getAppVersion() { return "3.4"; }',
    '@JavascriptInterface public String getAppVersion() { return "3.5"; }'
)
assert 'return "3.5"' in j
jp.write_text(j,encoding='utf-8')
