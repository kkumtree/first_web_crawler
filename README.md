# My First Web Crawler

## Change Log

- 2023.10.  
  - Python: ^3.11.5  
  - Dependency: Windows -> Linux/Unix(Ubuntu, MacOS)  
  - Modify cause of Website Changing 

## Purpose

- 의사결정을 위한 리스트업 대응
- API나 별도의 스프레드시트 파일이 제공되지 않아, 검색을 통해 제작함

## Dependency

### Quick guide 

1. Prerequisite APT repos (Ubuntu/Debian)

```bash
# Prerequisite
sudo apt-get install build-essential
sudo apt install -y \
    libedit-dev zlib1g zlib1g-dev libssl-dev libbz2-dev libsqlite3-dev
```

2. pyenv

```bash
# pyenv auto-install
curl https://pyenv.run | bash

# linking for .bashrc
cat <<EOF >> ~/.bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
EOF

# Show installable versions
pyenv install -l | grep 3.11
pyenv install 3.11.6
pyenv global 3.11.6
```

3. venv

```bash
# git clone --depth=1 https://github.com/kkumtree/first_web_crawler.git && cd first_web_crawler/
python -m venv .venv
pip install requests bs4 selenium pandas
```

4. execute

```bash
python main.py
# deactivate
```

### env

- ~~Windows OS~~ Linux | Mac
- python ^3.11.5

### library

- bs4, selenium, pandas

### daemon

- ~~chromedriver~~
- Selenium doesn't need chromedriver daemon as default, anymore.  

```shell
pip install requests
pip install bs4
pip install selenium
pip install pandas
```

## Performence

- ~~매우 낮은 성능, I/O를 매 행마다 하다보니 csv로 했음에도 3000행에 대해 20여분 소요~~  
  > 업데이트 이후, 속도가 빨라짐  

## Think about...

- 페이지 당 dataframe에 쌓아두고, csv append 한 번씩만 한다면 개선의 여지가 있을 것으로 판단
- 멀티 프로세싱 미적용
- 반복 기능에 대한 함수 분리가 덜 되어있음
- VSCode에서 구동, **init** 설정을 하지 않아 일반적 실행시 수정 필요
- dataframe에서 행, 열 전환 시 특정 함수 호출 시 오류가 발생하나,  
  원인을 생각하지 않고 해당 함수를 지워서 해결함. 나중에 알아봐야 할 것

## 작성일 및 소요시간(테스트 구동 포함)

- 2022-01-27 / 13:00 ~ 23:50 (approx. 11H)
