#include <bits/stdc++.h> 
#define N 4
using namespace std;

int counter = 0;

int arr[N];
bool isSafe(int x, int y){
	set<int> _set[N];

	for(int i=0; i<x; i++){
		for(int j=i; j<N; j++){
			_set[j].insert(arr[i]);		
			if(arr[i] + j - i < N)  _set[j].insert(arr[i] + j - i); 
			if(arr[i] + i - j >= 0) _set[j].insert(arr[i] + i - j);
		}
	}
	if(_set[x].count(y)) return false;
	return true;
}

void printBoard(){
	for(int i=0; i<N; i++){
		for(int j=0; j<N; j++){
			if(arr[j] == i) printf("Q ");
			else printf("X ");
		}
		printf("\n");
	}
	printf("\n");
}

void solve(int x, int y){
	if(x == N){
		printBoard();
		counter++;
		return;
	}
	if(x >= N || y >= N) return;

	if(isSafe(x,y)){
		arr[x] = y;
		solve(x + 1, 0);
	}
	arr[x] = -1;
	solve(x, y+1);

	return;
}

int main(){
	for(int i=0; i<N; ++i) arr[i] = -1;
	solve(0,0);
	printf("%d\n", counter);
}
