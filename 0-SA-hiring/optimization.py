# Q2. 멀티프로세싱과 성능 최적화
# 주어진 리스트의 숫자들에 대해
# 각 숫자가 소수인지 아닌지를
# 병렬 프로세스를 사용해 확인하는 프로그램을 작성하세요

import multiprocessing
import math

def is_prime(n) -> bool:
    for i in range(2, int(math.sqrt(n) + 1)): # 불필요한 계산 생략
        if n % i == 0:
            return False
    return True

def check_prime_numbers(numbers) -> list[bool]:
    with multiprocessing.Pool(16) as p:
        return p.map(is_prime, numbers) # 동시 실행 후 결과를 리스트로

numbers = [999999937, 999999893, 999999883, 999999797, 999999757]

# 병렬 프로세싱을 사용하여 각 숫자가 소수인지 확인하는 코드를 작성하세요.
if __name__ == '__main__':
    result = check_prime_numbers(numbers) # 리스트 결과를 받아오고

    print('소수 판정 결과:')
    for n, b in zip(numbers, result): # 대응되는 것끼리 출력
        print(f'{n}: {'소수입니다' if b else '소수가 아닙니다'}.')