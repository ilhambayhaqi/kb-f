# Tugas Kecerdasan Buatan F
## Tic Tac Toe (T3)
Pada tic tac toe yang dibuat, algoritma yang digunakan adalah minimax. Dimana bila kondisi player menang maka state tersebut bernilai -1, bila ai menang bernilai 1 dan bila seri maka bernilai 0.
```
	if(isWin(currState, 'X')) return -1;
	if(isWin(currState, 'O')) return 1;
	if(isDraw(currState)) return 0;
```
Pada algoritma minimax, maka ai akan melakukan traverse dan untuk setiap turn ai maka akan dipilih nilai yang maximal sedangkan ketika player turn akan dicari nilai paling minimalnya. Untuk fungsi ai mencari move terbaik sebagai berikut.
```
int getBestMove(string currState){ //AI
	string temp = currState;
	int bestVal = INT_MIN;
	//int bestMove = -1;
	vector<int> v;
	for(int i=0; i<9; i++){
		if(temp[i] == '_'){
			temp[i] = 'O';
			int moveVal = minimax(temp,false);
			temp[i] = '_';
            if(moveVal > bestVal){
                v.clear();
                v.push_back(i);
                //bestMove = i;
                bestVal = moveVal;
            }
            if(moveVal == bestVal){
            	v.push_back(i);
            }
		}
	}
	int randomIndex = rand() % v.size();
	return v[randomIndex];
	//return bestMove;
}
```
Sedangkan untuk algoritma Minimaxnya sebagai berikut.
```
int minimax(string currState , bool isMax){
	if(isWin(currState, 'X')) return -1;
	if(isWin(currState, 'O')) return 1;
	if(isDraw(currState)) return 0;

	if(isMax){
		int best = INT_MIN;
		for (int i = 0; i < 9; ++i){
			if(currState[i] == '_'){
				currState[i] = 'O';
				best = max(best, minimax(currState, !isMax));
				currState[i] = '_';
			}
		}
		return best;
	}
	else{
		int best = INT_MAX;
		for (int i = 0; i < 9; ++i){
			if(currState[i] == '_'){
				currState[i] = 'X';
				best = min(best, minimax(currState, !isMax));
				currState[i] = '_';
			}
		}
		return best;
	}
}
```
Pada minimax tersebut, ketika isMax == true maka akan membandingkan best saat ini dengan minimum pada setelahnnya untuk dicari nilai maksimalnya. Begitu pula bila isMax == false maka akan mencari nilai minimum dari best saat ini dengan maksimum pada state didalamnya.

## 4 Queen (T4)

Pada tugas 4, diminta untuk menggunakan CSP (constrain satisfaction problem) pada 4 queen dengan pendekatan forward checking.
Pada mulanya dilakukan pengecekan untuk kolom 0 dan 0 dan inisialisasi untuk set terpilih(diimplementasikan menggunakan array arr) sebagai berikut.
```
	for(int i=0; i<N; ++i) arr[i] = -1;
	solve(0,0);
```
Kemudian pada fungsi solve dilakukan rekursif dan untuk tiap x dan y yang di visit dilakukan pengecekan apakah safe atau tidak.
```
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
```
Untuk setiap tempat yang safe maka dilakukan update pada set terpilih (arr) dan melakukan pengecekan untuk x selanjutnya.
Bila tempat tersebut tidak safe maka dilakukan pengecekan untuk y selanjutnya. Bila tidak dapat memenuhi constraint yang ada maka dilakukan backtracking. Untuk fungsi pengecekan safe dengan forward checking menggunakan set dengan melakukan generate pada petak yang terkena serang oleh queen. Untuk fungsinya sebagai berikut.
```
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
```
Setelah seluruh constraint terpenuhi maka dilakukan print board sebagai berikut.
```
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
```




