#ifndef TYPES_INCLUDED
#define TYPES_INCLUDED
#include <map>

typedef std::pair<int, int> pii;

typedef unsigned long long Bitstring;

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

// Definitely not copied from SF
enum Value : int {
	VALUE_ZERO = 0,
    VALUE_INFINITE = 1000000,

	MATE = 100000,
	MATED = -100000,
	DRAWN = 0,

	PawnValueMg   =  100,  PawnValueEg   =  126,
	KnightValueMg =  325,  KnightValueEg =  310,
	BishopValueMg =  371,  BishopValueEg =  380,
	RookValueMg   =  563,  RookValueEg   =  609,
	QueenValueMg  = 1000,  QueenValueEg  = 1353,

	RESIGN = 1000
};

enum Depth : int {
	ONE_PLY = 1,

	DEPTH_ZERO          =  0,
	DEPTH_QS_NO_CHECKS  = -1,

	MAX_DEPTH = 69
};

enum Score : int { 
	SCORE_ZERO
};
constexpr Score make_score(int mg, int eg) {
  	return Score((int)((unsigned int)eg << 16) + mg);
}
inline Value eg_value(Score s) {
	union { uint16_t u; int16_t s; } eg = { uint16_t(unsigned(s + 0x8000) >> 16) };
	return Value(eg.s);
}

inline Value mg_value(Score s) {
	union { uint16_t u; int16_t s; } mg = { uint16_t(unsigned(s)) };
	return Value(mg.s);
}

#define ENABLE_BASE_OPERATORS_ON(T)                                \
constexpr T operator+(T d1, T d2) { return T(int(d1) + int(d2)); } \
constexpr T operator-(T d1, T d2) { return T(int(d1) - int(d2)); } \
constexpr T operator-(T d) { return T(-int(d)); }                  \
inline T& operator+=(T& d1, T d2) { return d1 = d1 + d2; }         \
inline T& operator-=(T& d1, T d2) { return d1 = d1 - d2; }

#define ENABLE_INCR_OPERATORS_ON(T)                                \
inline T& operator++(T& d) { return d = T(int(d) + 1); }           \
inline T& operator--(T& d) { return d = T(int(d) - 1); }

#define ENABLE_FULL_OPERATORS_ON(T)                                \
ENABLE_BASE_OPERATORS_ON(T)                                        \
constexpr T operator*(int i, T d) { return T(i * int(d)); }        \
constexpr T operator*(T d, int i) { return T(int(d) * i); }        \
constexpr T operator/(T d, int i) { return T(int(d) / i); }        \
constexpr int operator/(T d1, T d2) { return int(d1) / int(d2); }  \
inline T& operator*=(T& d, int i) { return d = T(int(d) * i); }    \
inline T& operator/=(T& d, int i) { return d = T(int(d) / i); }

ENABLE_FULL_OPERATORS_ON(Value)
ENABLE_FULL_OPERATORS_ON(Depth)
ENABLE_FULL_OPERATORS_ON(Score)

#undef ENABLE_FULL_OPERATORS_ON
#undef ENABLE_INCR_OPERATORS_ON
#undef ENABLE_BASE_OPERATORS_ON

/// Additional operators to add integers to a Value
constexpr Value operator+(Value v, int i) { return Value(int(v) + i); }
constexpr Value operator-(Value v, int i) { return Value(int(v) - i); }
inline Value& operator+=(Value& v, int i) { return v = v + i; }
inline Value& operator-=(Value& v, int i) { return v = v - i; }

#endif