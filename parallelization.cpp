// Matrix_Mul.cpp : 定义控制台应用程序的入口点。
#include <pmmintrin.h>
#include <stdlib.h>
#include <algorithm>
#include <windows.h>
#include <time.h>
#include <xmmintrin.h>
#include <iostream>
#include <pthread.h>
#include <math.h>
#include <vector>
#pragma comment(lib, "pthreadVC2.lib")
using namespace std;
const int maxN = 10000;// magnitude of matrix
float a[maxN][maxN];
float b[maxN];
float c[maxN];
const int THREAD_NUM = 4;//n4mber of threads
typedef struct {
	int threadId;
} threadParm_t;
pthread_mutex_t mutex_task;
pthread_mutex_t	mutex;
long long head, freq, tail;// timers
void init(int n)
{
	for (int i = 0; i < n; ++i) {
		for (int j = 0; j < n; ++j) {
			a[i][j] = (float)rand();
		}
		b[i] = (float)rand();
	}
}
void print(int n, float a[][maxN]) {
	if (n < 10){
		for (int i = 0; i < n; ++i) {
			for (int j = 0; j < n; ++j)
				cout << a[i][j] << " ";
			cout << endl;
		}
	}
	else
	{
		for (int i = 0; i < 10; ++i) {
			for (int j = 0; j < 10; ++j)
				cout << a[i][j] << " ";
			cout << endl;
		}
	}
}
void mul(int n, float a[][maxN], float b[], float c[]) {
	for (int i = 0; i < n; ++i) {
		c[i] = 0.0;
		for (int k = 0; k < n; ++k) {
			c[i] += a[i][k] * b[k];
		}
	}
}
int next_arr = 0;
int key = 0;
/***pthread线程内执行函数***/
void *mypthread(void *parm)
{
	//key++;
	threadParm_t *p = (threadParm_t *)parm;
	int r = p->threadId;
	int task = 0;
	while (1) {
		__m128 t1, t2, sum;
		pthread_mutex_lock(&mutex_task);//上锁防止分配task时被其他线程打断
		task = next_arr++;
		pthread_mutex_unlock(&mutex_task);
		if (task >= maxN) break;
		int k;
		c[task] = 0.0;
		sum = _mm_setzero_ps();
		for (k = 0; k <= maxN - 4; k += 4) {//sum every 4th elements
			t1 = _mm_loadu_ps(a[task] + k);
			t2 = _mm_loadu_ps(b + k);
			t1 = _mm_mul_ps(t1, t2);
			sum = _mm_add_ps(sum, t1);
		}
		sum = _mm_hadd_ps(sum, sum);
		sum = _mm_hadd_ps(sum, sum);
		_mm_store_ss(c, sum);
		for (; k < maxN; k++) {//handle the last n%4 elements
			c[task] += a[task][k] * b[k];
		}

	}

	pthread_mutex_lock(&mutex);////上锁防止计算结束时间被其他线程打断
	QueryPerformanceCounter((LARGE_INTEGER *)&tail);
	printf("Thread %d: %lfms.\n", r, (tail - head) * 1000.0 / freq);
	pthread_mutex_unlock(&mutex);

	pthread_exit(nullptr);
	return NULL;
}
/***pthread线程执行主函数***/
void thread_execute() {
	QueryPerformanceCounter((LARGE_INTEGER *)&head);//计时开始
	pthread_t thread[THREAD_NUM];
	threadParm_t threadParm[THREAD_NUM];

	int j = 0;
	next_arr = j;
	for (int i = 0; i < THREAD_NUM; i++)
	{
		threadParm[i].threadId = i;
		pthread_create(&thread[i], nullptr, mypthread, (void *)&threadParm[i]);//线程创建
	}
	for (int i = 0; i < THREAD_NUM; i++)
	{
		pthread_join(thread[i], nullptr);//线程间同步
	}

	pthread_mutex_destroy(&mutex);//线程消除
	pthread_mutex_destroy(&mutex_task);
}
/**矩阵相乘SSE算法**/
void sse_mul(int n, float a[][maxN], float b[], float c[]){
	__m128 t1, t2, sum;
	for (int i = 0; i < n; ++i){
		c[i] = 0.0;
		sum = _mm_setzero_ps();
		for (int k = n - 4; k >= 0; k -= 4){     // sum every 4 elements
			t1 = _mm_loadu_ps(a[i] + k);
			t2 = _mm_loadu_ps(b + k);
			t1 = _mm_mul_ps(t1, t2);
			sum = _mm_add_ps(sum, t1);
		}
		sum = _mm_hadd_ps(sum, sum);
		sum = _mm_hadd_ps(sum, sum);
		_mm_store_ss(c, sum);
		for (int k = (n % 4) - 1; k >= 0; --k){    // handle the last n%4 elements
			c[i] += a[i][k] * b[i];
		}
	} 
}
void mul_omp(int n, float a[][maxN], float b[], float c[]) {
	for (int i = 0; i < n; ++i) {
		c[i] = 0.0;
#pragma omp parallel for num_threads(THREAD_NUM)
		for (int k = 0; k < n; ++k) {
			c[i] += a[i][k] * b[k];
		}
	}
}
void sse_mul_omp(int n, float a[][maxN], float b[], float c[]){
	__m128 t1, t2, sum;
	for (int i = 0; i < n; ++i){
		c[i] = 0.0;
#pragma omp parallel for num_threads(THREAD_NUM)
		sum = _mm_setzero_ps();
		for (int k = n - 4; k >= 0; k -= 4){     // sum every 4 elements
			t1 = _mm_loadu_ps(a[i] + k);
			t2 = _mm_loadu_ps(b + k);
			t1 = _mm_mul_ps(t1, t2);
			sum = _mm_add_ps(sum, t1);
		}
		sum = _mm_hadd_ps(sum, sum);
		sum = _mm_hadd_ps(sum, sum);
		_mm_store_ss(c, sum);
		for (int k = (n % 4) - 1; k >= 0; --k){    // handle the last n%4 elements
			c[i] += a[i][k] * b[k];
		}
	}
}
int main(int argc, char *argv[])
{
	printf("waiting......\n");
	QueryPerformanceFrequency((LARGE_INTEGER *)&freq);
	init(maxN);
	mutex_task = PTHREAD_MUTEX_INITIALIZER;
	mutex = PTHREAD_MUTEX_INITIALIZER;
	QueryPerformanceCounter((LARGE_INTEGER *)&head);
	mul(maxN, a, b, c);
	QueryPerformanceCounter((LARGE_INTEGER *)&tail);
	printf("MUL: %lfms.\n", (tail - head) * 1000.0 / freq);
	QueryPerformanceCounter((LARGE_INTEGER *)&head);
	sse_mul(maxN, a, b, c);
	QueryPerformanceCounter((LARGE_INTEGER *)&tail);
	printf("SSE: %lfms.\n", (tail - head) * 1000.0 / freq);	
	QueryPerformanceCounter((LARGE_INTEGER *)&head);
	sse_mul_omp(maxN, a, b, c);
	QueryPerformanceCounter((LARGE_INTEGER *)&tail);
	printf("OMP_SSE: %lfms.\n", (tail - head) * 1000.0 / freq);
	//print(maxN, c);
	cout << endl << endl;
	printf("Pthread:\n");
	thread_execute();
	system("pause");
	//print(maxN, c);
	//cout << key;
}