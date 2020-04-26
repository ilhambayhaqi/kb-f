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


## 4 Queen (T4)
