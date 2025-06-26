# Q1. 프로세스 및 네트워크 모니터링


## 1. CPU 사용률이 80% 이상인 프로세스만 표시하는 명령어를 작성하세요.
```bash
$ ps -eo %cpu,args | awk '$1 >= 80 {print}'
```
[1]

## 2. 현재 시스템에서 네트워크 포트 80번을 사용하는 프로세스를 찾아 종료하는 명령어를 작성하세요.
```bash
$ netstat -tulpn | grep :80
```
[2]

## 3. 특정 프로세스 apache2의 메모리 사용량과 네트워크 트래픽을 5초 간격으로 실시간으로 모니터링하는 방법을 설명하고, 해당 명령어를 작성하세요.
1. 5초 간격으로 다른 명령어를 실행하는 명령어를 실행 `watch`
2. apache2의 process ID를 구함 `pidof`
3. (1.) 명령어의 argument로 (2.) 프로세스의 메모리를 출력하는 명령어를 넣음
4. 네트워크 트래픽은 다른 명령어가 필요함. `ifstat`으로 받고 네트워크 트래픽 부분만 추출
5. 이들을 하나의 명령으로 통합. 이때 `'` 는 escape 되지 않으므로 `"'"`으로 감싸줘야 함.
```bash
$ watch -n 5 'ps -p $(pidof apache2) -o %mem && ifstat 1 1 | tail -1 | awk '"'"'{ print $1,$2 }'"'"
```
[3] [4] [5]

---

[^1] [stackexchange](https://unix.stackexchange.com/questions/295599/how-to-show-processes-that-use-more-than-30-cpu)

[^2] [nixCraft](https://www.cyberciti.biz/faq/find-linux-what-running-on-port-80-command/)

[^3] [Linux man page](https://linux.die.net/man/1/watch)

[^4] [Linux man page](https://linux.die.net/man/1/ps)

[^5] [stackoverflow](https://stackoverflow.com/questions/38056120/how-to-get-network-traffic-as-one-number-on-linux)

[^6] [stackoverflow](https://stackoverflow.com/questions/1250079/how-to-escape-single-quotes-within-single-quoted-strings)