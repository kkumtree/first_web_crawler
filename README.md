# My First Web Crawler

## Purpose

- 의사결정을 위한 리스트업 대응
- API나 별도의 스프레드시트 파일이 제공되지 않아, 검색을 통해 제작함

## Dependency

### env

- Windows OS / python ^3.0.0

### library

- bs4, selenium, pandas

### daemon

- chromedriver

```shell
pip install requests
pip install bs4
pip install selenium
pip install pandas
```

## Performence

- 매우 낮은 성능, I/O를 매 행마다 하다보니 csv로 했음에도 3000행에 대해 20여분 소요

## Think about...

- 페이지 당 dataframe에 쌓아두고, csv append 한 번씩만 한다면 개선의 여지가 있을 것으로 판단
- 멀티 프로세싱 미적용
- 반복 기능에 대한 함수 분리가 덜 되어있음
- VSCode에서 구동, **init** 설정을 하지 않아 일반적 실행시 수정 필요
- dataframe에서 행, 열 전환 시 특정 함수 호출 시 오류가 발생하나,  
  원인을 생각하지 않고 해당 함수를 지워서 해결함. 나중에 알아봐야 할 것

## 작성일 및 소요시간(테스트 구동 포함)

- 2022-01-28 / 13:00 ~ 23:50 (approx. 11H)
