#ifndef STATE_H_INCLUDED
#define STATE_H_INCLUDED

#include <iostream>
#include <vector>
#include <fstream>
#include <string>

#include "Eval_info.h"
#include "Transpose_info.h"

#define n 8
#define BP -1
#define WP 1
#define BN -2
#define WN 2
#define BB -3
#define WB 3
#define BR -4
#define WR 4
#define BQ -5
#define WQ 5
#define BK -6
#define WK 6

extern int default_board[8][8];

extern int dr_knight[8], dc_knight[8], dr_bishop[4], dc_bishop[4], dr_rook[4],
dc_rook[4], dr_queen[8], dc_queen[8], dr_king[8], dc_king[8];

class state {
public:
	bool out_of_bounds(int row, int column) {
		if (row < 0) return true;
		if (column < 0) return true;
		if (row >= n) return true;
		if (column >= n) return true;
		return false;
	}

	int board[8][8];
	long long board_hash;

	void replace_board(int row, int col, int piece) {
		board_hash = (board_hash - f_exp2(8 * row + col) * (board[row][col] + 6) + SAFETY) % MOD;
		board[row][col] = piece;
		board_hash = (board_hash + f_exp2(8 * row + col) * (board[row][col] + 6) + SAFETY) % MOD;
	}

	int black_king_moved = false;
	int black_lrook_moved = false;
	int black_rrook_moved = false;
	int white_king_moved = false;
	int white_lrook_moved = false;
	int white_rrook_moved = false;
	bool white_castled = false, black_castled = false;
	int fifty_move;
	bool to_move; // true if white to move

	state() {
		fifty_move = 0;
		doubled_black = 0;
		doubled_white = 0;
		to_move = true;
		for (int i = 0; i < 8; i++) {
			for (int j = 0; j < 8; j++) {
				board[i][j] = default_board[i][j];
			}
		}
		board_hash = 0;
		for (int i = 0; i < 8; i++) {
			for (int j = 0; j < 8; j++) {
				board_hash = (board_hash + f_exp2(8 * i + j) * (board[i][j] + 6)) % MOD;
			}
		}
	}

	std::string to_piece(int x);
	int piece_to_int(char c);
	std::string move_to_string(int move);

	bool operator==(state s) {
		if (s.to_move != to_move) return false;
		for (int i = 0; i < 8; i++) {
			for (int j = 0; j < 8; j++) {
				if (s.board[i][j] != board[i][j]) return false;
			}
		}
		return true;
	}

	void print();

	int parse_move(std::string move);

	void make_move(int move);
	void unmake_move(int move);

	int attacking(int row, int col, bool color);

	std::vector <int> list_moves();

	bool quiescent();

	bool adjucation();

	int mate();
};

extern state curr_state;
#endif // !STATE_H_INCLUDED
