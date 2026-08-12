// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
const SCOREBOARD_KEY = 'sudokuTopScores';
let puzzle = [];
let hintCount = 0;
let elapsedSeconds = 0;
let timerInterval = null;
let currentDifficulty = 'medium';
let scoreAdded = false;
const THEME_KEY = 'sudokuTheme';

function applyTheme(theme) {
  const body = document.body;
  body.classList.remove('light-theme', 'dark-theme');
  body.classList.add(`${theme}-theme`);
  const toggleButton = document.getElementById('theme-toggle');
  if (toggleButton) {
    toggleButton.setAttribute('aria-pressed', theme === 'dark');
    toggleButton.textContent = theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
  }
}

function getSavedTheme() {
  const saved = localStorage.getItem(THEME_KEY);
  if (saved === 'light' || saved === 'dark') {
    return saved;
  }
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

function initializeTheme() {
  applyTheme(getSavedTheme());
}

function toggleTheme() {
  const currentTheme = document.body.classList.contains('dark-theme') ? 'dark' : 'light';
  const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
  localStorage.setItem(THEME_KEY, nextTheme);
  applyTheme(nextTheme);
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      const blockRow = Math.floor(i / 3);
      const blockCol = Math.floor(j / 3);
      const blockStyle = (blockRow + blockCol) % 2 === 0 ? 'block-even' : 'block-odd';
      input.classList.add(blockStyle);
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
        clearCellFeedback();
        markConflicts();
        updateMessage('');
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  hintCount = 0;
  scoreAdded = false;
  updateHintDisplay();
  createBoardElement();
  clearCellFeedback();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.classList.add('prefilled');
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
}

function getBoardFromInputs() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  return board;
}

function clearCellFeedback() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (const inp of inputs) {
    inp.classList.remove('incorrect', 'conflict');
  }
}

function updateMessage(text, color = '#d32f2f') {
  const msg = document.getElementById('message');
  if (!msg) return;
  msg.innerText = text;
  msg.style.color = color;
}

function markConflicts() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = getBoardFromInputs();
  const conflictIndexes = new Set();

  for (let row = 0; row < SIZE; row++) {
    for (let col = 0; col < SIZE; col++) {
      const value = board[row][col];
      if (!value) continue;
      for (let c = 0; c < SIZE; c++) {
        if (c !== col && board[row][c] === value) {
          conflictIndexes.add(row * SIZE + col);
          conflictIndexes.add(row * SIZE + c);
        }
      }
      for (let r = 0; r < SIZE; r++) {
        if (r !== row && board[r][col] === value) {
          conflictIndexes.add(row * SIZE + col);
          conflictIndexes.add(r * SIZE + col);
        }
      }
      const startRow = Math.floor(row / 3) * 3;
      const startCol = Math.floor(col / 3) * 3;
      for (let r = startRow; r < startRow + 3; r++) {
        for (let c = startCol; c < startCol + 3; c++) {
          if ((r !== row || c !== col) && board[r][c] === value) {
            conflictIndexes.add(row * SIZE + col);
            conflictIndexes.add(r * SIZE + c);
          }
        }
      }
    }
  }

  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.classList.toggle('conflict', conflictIndexes.has(idx));
  }
}

function updateHintDisplay() {
  const countDisplay = document.getElementById('hint-count');
  if (countDisplay) {
    countDisplay.innerText = hintCount;
  }
}

function formatTime(seconds) {
  const minutes = String(Math.floor(seconds / 60)).padStart(2, '0');
  const secs = String(seconds % 60).padStart(2, '0');
  return `${minutes}:${secs}`;
}

function updateTimerDisplay() {
  const timerElement = document.getElementById('elapsed-time');
  if (timerElement) {
    timerElement.innerText = formatTime(elapsedSeconds);
  }
}

function saveScores(scores) {
  localStorage.setItem(SCOREBOARD_KEY, JSON.stringify(scores));
}

function loadScores() {
  try {
    const stored = localStorage.getItem(SCOREBOARD_KEY);
    if (!stored) {
      return [];
    }
    const parsed = JSON.parse(stored);
    if (!Array.isArray(parsed)) {
      return [];
    }
    return parsed.filter((entry) =>
      entry && typeof entry.name === 'string' &&
      typeof entry.timeSeconds === 'number' &&
      typeof entry.difficulty === 'string' &&
      typeof entry.hints === 'number'
    );
  } catch (err) {
    return [];
  }
}

function formatScoreEntry(entry) {
  return {
    name: entry.name,
    timeSeconds: entry.timeSeconds,
    difficulty: entry.difficulty,
    hints: entry.hints
  };
}

function renderScoreboard() {
  const scores = loadScores();
  const body = document.getElementById('scoreboard-body');
  const empty = document.getElementById('scoreboard-empty');
  if (!body || !empty) {
    return;
  }
  body.innerHTML = '';
  if (scores.length === 0) {
    empty.style.display = 'block';
    return;
  }
  empty.style.display = 'none';
  scores.forEach((entry, index) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${index + 1}</td>
      <td>${entry.name}</td>
      <td>${formatTime(entry.timeSeconds)}</td>
      <td>${entry.difficulty.charAt(0).toUpperCase() + entry.difficulty.slice(1)}</td>
      <td>${entry.hints}</td>
    `;
    body.appendChild(row);
  });
}

function addScore(name, difficulty, timeSeconds, hints) {
  const scores = loadScores();
  scores.push(formatScoreEntry({name, difficulty, timeSeconds, hints}));
  scores.sort((a, b) => a.timeSeconds - b.timeSeconds);
  const topScores = scores.slice(0, 10);
  saveScores(topScores);
  renderScoreboard();
}

// Show an in-page modal to get the player's name. Returns a Promise that resolves to the chosen name (or 'Anonymous').
function showNameModal(defaultName = '') {
  return new Promise((resolve) => {
    const modal = document.getElementById('name-modal');
    const input = document.getElementById('player-name-input');
    const saveBtn = document.getElementById('player-name-save');
    const cancelBtn = document.getElementById('player-name-cancel');
    if (!modal || !input || !saveBtn || !cancelBtn) {
      resolve(defaultName || 'Anonymous');
      return;
    }
    input.value = defaultName || '';
    modal.classList.add('show');
    modal.setAttribute('aria-hidden', 'false');
    // focus input
    setTimeout(() => input.focus(), 50);

    function cleanup() {
      modal.classList.remove('show');
      modal.setAttribute('aria-hidden', 'true');
      saveBtn.removeEventListener('click', onSave);
      cancelBtn.removeEventListener('click', onCancel);
      input.removeEventListener('keydown', onKey);
    }

    function onSave() {
      const name = input.value.trim() || 'Anonymous';
      cleanup();
      resolve(name);
    }

    function onCancel() {
      cleanup();
      resolve('Anonymous');
    }

    function onKey(e) {
      if (e.key === 'Enter') onSave();
      if (e.key === 'Escape') onCancel();
    }

    saveBtn.addEventListener('click', onSave);
    cancelBtn.addEventListener('click', onCancel);
    input.addEventListener('keydown', onKey);
  });
}

function clearTimer() {
  if (timerInterval !== null) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}

function resetTimer() {
  clearTimer();
  elapsedSeconds = 0;
  updateTimerDisplay();
}

function startTimer() {
  resetTimer();
  timerInterval = setInterval(() => {
    elapsedSeconds += 1;
    updateTimerDisplay();
  }, 1000);
}

function stopTimer() {
  clearTimer();
}

async function newGame() {
  const difficultySelect = document.getElementById('difficulty');
  const difficulty = difficultySelect ? difficultySelect.value : 'medium';
  currentDifficulty = difficulty;
  const res = await fetch(`/new?difficulty=${encodeURIComponent(difficulty)}`);
  const data = await res.json();
  renderPuzzle(data.puzzle);
  updateMessage('');
  startTimer();
}

async function requestHint() {
  const board = getBoardFromInputs();
  const res = await fetch('/hint', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  if (data.error) {
    updateMessage(data.error, '#d32f2f');
    return;
  }
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const idx = data.row * SIZE + data.col;
  const inp = inputs[idx];
  inp.value = data.value;
  inp.disabled = true;
  inp.classList.add('hinted');
  hintCount += 1;
  updateHintDisplay();
  clearCellFeedback();
  updateMessage('');
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  if (data.error) {
    updateMessage(data.error, '#d32f2f');
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0] * SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.classList.remove('incorrect');
    if (incorrect.has(idx)) {
      inp.classList.add('incorrect');
    }
  }
  if (data.complete && incorrect.size === 0) {
    updateMessage('Congratulations! You solved it!', '#388e3c');
    stopTimer();
    if (!scoreAdded) {
      // Use in-page modal to request player's name (prompt() is not supported in some browsers)
      try {
        const name = await showNameModal('');
        addScore(name, currentDifficulty, elapsedSeconds, hintCount);
      } catch (err) {
        // Fallback to anonymous if anything goes wrong
        addScore('Anonymous', currentDifficulty, elapsedSeconds, hintCount);
      }
      scoreAdded = true;
    }
  } else if (incorrect.size > 0) {
    updateMessage('Some cells are incorrect.', '#d32f2f');
  } else {
    updateMessage('Keep going! Some cells are still empty.', '#d32f2f');
  }
}

// Wire buttons
window.addEventListener('load', () => {
  const themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', toggleTheme);
  }
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('hint-button').addEventListener('click', requestHint);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  initializeTheme();
  renderScoreboard();
  // initialize
  newGame();
});