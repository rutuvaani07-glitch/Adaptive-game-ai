DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>X vs O — Tic Tac Toe</title>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --x-color: #E24B4A;
    --o-color: #378ADD;
    --bg: #0e0e0e;
    --surface: #1a1a1a;
    --surface2: #232323;
    --border: rgba(255,255,255,0.1);
    --border2: rgba(255,255,255,0.2);
    --text: #f0ede8;
    --muted: #888;
    --win-bg: rgba(99,200,80,0.12);
    --win-border: rgba(99,200,80,0.5);
    --cell-size: 130px;
    --gap: 12px;
  }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'DM Mono', monospace;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
  }

  /* subtle grid background */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
      linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
  }

  .wrap {
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
    width: 100%;
    max-width: 480px;
  }

  .title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 64px;
    letter-spacing: 8px;
    line-height: 1;
    color: var(--text);
  }
  .title .tx { color: var(--x-color); }
  .title .to { color: var(--o-color); }

  .mode-row {
    display: flex;
    gap: 8px;
  }

  .mode-btn {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 7px 18px;
    border: 1px solid var(--border2);
    border-radius: 8px;
    background: transparent;
    color: var(--muted);
    cursor: pointer;
    transition: all 0.15s;
  }
  .mode-btn:hover { background: var(--surface2); color: var(--text); }
  .mode-btn.active {
    background: rgba(55,138,221,0.15);
    border-color: rgba(55,138,221,0.5);
    color: var(--o-color);
  }

  .score-row {
    display: flex;
    gap: 2rem;
    align-items: center;
  }
  .score-item { display: flex; flex-direction: column; align-items: center; gap: 4px; }
  .score-label { font-size: 11px; letter-spacing: 2px; text-transform: uppercase; color: var(--muted); }
  .score-val { font-family: 'Bebas Neue', sans-serif; font-size: 36px; line-height: 1; }
  .score-val.x { color: var(--x-color); }
  .score-val.o { color: var(--o-color); }
  .score-val.d { color: var(--muted); }
  .score-divider { width: 1px; height: 44px; background: var(--border); }

  .turn-row {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    min-height: 20px;
  }
  .turn-dot {
    width: 10px; height: 10px; border-radius: 50%;
    transition: background 0.2s;
  }

  .board {
    display: grid;
    grid-template-columns: repeat(3, var(--cell-size));
    grid-template-rows: repeat(3, var(--cell-size));
    gap: var(--gap);
  }

  .cell {
    width: var(--cell-size);
    height: var(--cell-size);
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 62px;
    line-height: 1;
    transition: background 0.12s, transform 0.1s, border-color 0.12s;
    user-select: none;
  }
  .cell:hover:not(.filled) {
    background: var(--surface2);
    border-color: var(--border2);
    transform: scale(1.05);
  }
  .cell.filled { cursor: default; }
  .cell.x { color: var(--x-color); }
  .cell.o { color: var(--o-color); }
  .cell.win-cell {
    background: var(--win-bg);
    border-color: var(--win-border);
  }

  .pop { animation: pop 0.2s cubic-bezier(.3,1.6,.5,1) forwards; }
  @keyframes pop {
    0% { transform: scale(0.3); opacity: 0; }
    100% { transform: scale(1); opacity: 1; }
  }

  .status {
    font-size: 13px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--muted);
    min-height: 20px;
    transition: color 0.2s;
  }
  .status.win { color: #63c850; }
  .status.draw { color: #e8a53a; }

  .btn-row { display: flex; gap: 10px; }
  .action-btn {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 9px 22px;
    border: 1px solid var(--border2);
    border-radius: 8px;
    background: transparent;
    color: var(--text);
    cursor: pointer;
    transition: all 0.15s;
  }
  .action-btn:hover { background: var(--surface2); }
  .action-btn:active { transform: scale(0.97); }

  @media (max-width: 500px) {
    :root { --cell-size: 100px; }
    .title { font-size: 50px; }
  }
</style>
</head>
<body>
<div class="wrap">
  <div class="title"><span class="tx">X</span> vs <span class="to">O</span></div>

  <div class="mode-row">
    <button class="mode-btn active" id="btn-2p" onclick="setMode('2p')">2 players</button>
    <button class="mode-btn" id="btn-ai" onclick="setMode('ai')">vs CPU</button>
  </div>

  <div class="score-row">
    <div class="score-item">
      <span class="score-label">X</span>
      <span class="score-val x" id="sx">0</span>
    </div>
    <div class="score-divider"></div>
    <div class="score-item">
      <span class="score-label">draws</span>
      <span class="score-val d" id="sd">0</span>
    </div>
    <div class="score-divider"></div>
    <div class="score-item">
      <span class="score-label">O</span>
      <span class="score-val o" id="so">0</span>
    </div>
  </div>

  <div class="turn-row">
    <div class="turn-dot" id="turn-dot"></div>
    <span id="turn-text">X's turn</span>
  </div>

  <div class="board" id="board"></div>
  <div class="status" id="status"></div>

  <div class="btn-row">
    <button class="action-btn" onclick="resetGame()">new game</button>
    <button class="action-btn" onclick="resetAll()">reset scores</button>
  </div>
</div>

<script>
  let board = ['','','','','','','','',''];
  let current = 'X';
  let gameOver = false;
  let mode = '2p';
  let scores = { X: 0, O: 0, D: 0 };
  const wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];

  function setMode(m) {
    mode = m;
    document.getElementById('btn-2p').classList.toggle('active', m === '2p');
    document.getElementById('btn-ai').classList.toggle('active', m === 'ai');
    resetGame();
  }

  function buildBoard() {
    const b = document.getElementById('board');
    b.innerHTML = '';
    board.forEach((_, i) => {
      const c = document.createElement('div');
      c.className = 'cell';
      c.id = 'c' + i;
      c.onclick = () => play(i);
      b.appendChild(c);
    });
  }

  function updateTurn() {
    const dot = document.getElementById('turn-dot');
    const txt = document.getElementById('turn-text');
    dot.style.background = current === 'X' ? 'var(--x-color)' : 'var(--o-color)';
    if (gameOver) { txt.textContent = ''; dot.style.opacity = '0'; return; }
    dot.style.opacity = '1';
    if (mode === 'ai' && current === 'O') txt.textContent = 'CPU thinking...';
    else txt.textContent = current + "'s turn";
  }

  function play(i) {
    if (board[i] || gameOver) return;
    if (mode === 'ai' && current === 'O') return;
    makeMove(i);
    if (mode === 'ai' && !gameOver) setTimeout(aiMove, 350);
  }

  function makeMove(i) {
    board[i] = current;
    const cell = document.getElementById('c' + i);
    cell.textContent = current;
    cell.classList.add('filled', current.toLowerCase());
    void cell.offsetWidth;
    cell.classList.add('pop');
    const w = checkWin();
    if (w) {
      gameOver = true;
      w.forEach(idx => document.getElementById('c' + idx).classList.add('win-cell'));
      setStatus(current + ' wins!', 'win');
      scores[current]++;
      updateScore();
      updateTurn();
    } else if (board.every(x => x)) {
      gameOver = true;
      setStatus("it's a draw", 'draw');
      scores.D++;
      updateScore();
      updateTurn();
    } else {
      current = current === 'X' ? 'O' : 'X';
      updateTurn();
    }
  }

  function aiMove() {
    const best = minimax(board, 'O');
    makeMove(best.idx);
  }

  function minimax(b, player) {
    const opp = player === 'O' ? 'X' : 'O';
    if (checkWinFor(b, 'O')) return { score: 10 };
    if (checkWinFor(b, 'X')) return { score: -10 };
    if (b.every(x => x)) return { score: 0 };
    const moves = [];
    b.forEach((v, i) => {
      if (!v) {
        const nb = [...b];
        nb[i] = player;
        const res = minimax(nb, opp);
        moves.push({ idx: i, score: res.score });
      }
    });
    return player === 'O'
      ? moves.reduce((a, m) => m.score > a.score ? m : a)
      : moves.reduce((a, m) => m.score < a.score ? m : a);
  }

  function checkWin() {
    for (const [a, b, c] of wins) {
      if (board[a] && board[a] === board[b] && board[a] === board[c]) return [a, b, c];
    }
    return null;
  }

  function checkWinFor(b, p) {
    for (const [a, bv, c] of wins) {
      if (b[a] === p && b[bv] === p && b[c] === p) return true;
    }
    return false;
  }

  function setStatus(msg, cls) {
    const s = document.getElementById('status');
    s.textContent = msg;
    s.className = 'status' + (cls ? ' ' + cls : '');
  }

  function updateScore() {
    document.getElementById('sx').textContent = scores.X;
    document.getElementById('so').textContent = scores.O;
    document.getElementById('sd').textContent = scores.D;
  }

  function resetGame() {
    board = ['','','','','','','','',''];
    current = 'X';
    gameOver = false;
    setStatus('');
    buildBoard();
    updateTurn();
  }

  function resetAll() {
    scores = { X: 0, O: 0, D: 0 };
    updateScore();
    resetGame();
  }

  buildBoard();
  updateTurn();
</script>
</body>
</html>
