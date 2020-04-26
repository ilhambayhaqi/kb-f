#include <bits/stdc++.h>
using namespace std;

void printBoard(string str){
	for (int i = 0; i < 3; ++i){
		for (int j = 0; j < 3; ++j)
		{
			cout<<str[i*3+j]<<" ";
		}
		cout<<endl;
	}
	cout<<endl;
}

bool isValid(string currState, int idx){
	if(currState[idx] == '_') return true;
	return false;
}

void setBoard(string &currState, int idx, char symbol){
	currState[idx] = symbol;
}

bool checkWin(string currState, char a, char b, char c, char symbol){
	if(currState[a]==symbol && currState[b]==symbol && currState[c]==symbol) return true;
	return false;
}

bool isWin(string currState, char symbol){
	if(checkWin(currState,0,1,2,symbol)) return true;
	if(checkWin(currState,3,4,5,symbol)) return true;
	if(checkWin(currState,6,7,8,symbol)) return true;
	if(checkWin(currState,0,3,6,symbol)) return true;
	if(checkWin(currState,1,4,7,symbol)) return true;
	if(checkWin(currState,2,5,8,symbol)) return true;
	if(checkWin(currState,0,4,8,symbol)) return true;
	if(checkWin(currState,2,4,6,symbol)) return true;
	return false;
}

bool isDraw(string currState){
	if(!isWin(currState, 'X') && !isWin(currState, 'O')){
		for(int i=0; i<9; i++) {
			if(currState[i] == '_')  return false;
		}
		return true;
	}
	return false;
}

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

void play(string currState, bool isHuman){
	int posInput;
	printBoard(currState);
	for(int i=0; i<9; i++){
		if(isHuman) printf("Your Turn\n");
		if(isHuman){
			printf("Input (1-9) : ");
			cin>>posInput;
			posInput--;
			while(posInput < 0 || posInput > 8 || !isValid(currState, posInput)){
				printf("Input (1-9) : ");
				cin>>posInput;
				posInput--;
			}

			setBoard(currState, posInput, 'X');
			if(isWin(currState, 'X')) {
				printBoard(currState);
				printf("You Win\n");
				break;
			}
		}
		else{
			printf("Opponent move\n");
			setBoard(currState, getBestMove(currState), 'O');
			if(isWin(currState, 'O')) {
				printBoard(currState);
				printf("You Lose\n");
				break;
			}
		}
		isHuman = !isHuman;
		printBoard(currState);
	}
	if(isDraw(currState)) printf("Tie!!\n");
}

int main(int argc, char const *argv[])
{
	string currState = "_________";
	char turn;

	cout<<endl<<"You -> X | CPU -> O";
	cout<<endl<<"Select Turn : X -> Player first | O -> CPU first: ";
	cin>>turn;
	if(turn == 'X'){ //Human
		play(currState, true);
	}
	else if(turn == 'O'){
		play(currState, false);
	}

	return 0;
}
