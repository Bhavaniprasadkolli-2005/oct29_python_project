
from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NEON RUNNER | Dino Survival</title>

<style>
* { box-sizing: border-box; }

:root {
    --cyan: #65f7ff;
    --orange: #ff9d5c;
    --bg: #070a18;
}

body {
    margin: 0;
    min-height: 100vh;
    background:
        radial-gradient(ellipse at 50% 0%, #20284d 0%, #0b1024 45%, #03040b 100%);
    color: #f4f7ff;
    font-family: "Segoe UI", Arial, sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
    padding: 24px;
}

.game-shell {
    width: min(1100px, 100%);
}

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
    margin-bottom: 20px;
}

.brand {
    font-size: 13px;
    letter-spacing: 5px;
    color: var(--cyan);
    font-weight: 800;
}

.subtitle {
    color: #929dbd;
    font-size: 12px;
    letter-spacing: 2px;
    margin-top: 7px;
}

.status {
    border: 1px solid #65f7ff44;
    border-radius: 30px;
    padding: 10px 15px;
    color: var(--cyan);
    font-size: 11px;
    letter-spacing: 2px;
    background: #65f7ff0b;
    white-space: nowrap;
}

.game-card {
    position: relative;
    overflow: hidden;
    border: 1px solid #8499d72b;
    border-radius: 18px;
    background: #080c20;
    box-shadow: 0 25px 100px #0009, 0 0 45px #425dff0c;
}

.hud {
    position: absolute;
    top: 20px;
    left: 24px;
    right: 24px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    z-index: 3;
    pointer-events: none;
}

.hud-label {
    color: #91a1c6;
    font-size: 10px;
    letter-spacing: 3px;
}

.score {
    color: var(--cyan);
    font-size: 27px;
    font-weight: 800;
    margin-top: 5px;
    text-shadow: 0 0 18px #65f7ff66;
    font-variant-numeric: tabular-nums;
}

.best { text-align: right; }

.best .score {
    color: #ffd6a5;
    font-size: 20px;
}

canvas {
    display: block;
    width: 100%;
    height: auto;
    aspect-ratio: 1000 / 440;
    cursor: pointer;
    touch-action: manipulation;
}

.overlay {
    position: absolute;
    inset: 0;
    z-index: 2;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    background: linear-gradient(#080b1a20, #080b1ac9);
    padding: 20px;
}

.overlay.hidden { display: none; }

.panel {
    max-width: 450px;
    margin-top: 35px;
}

.eyebrow {
    color: var(--orange);
    letter-spacing: 5px;
    font-size: 10px;
    font-weight: 700;
}

h1 {
    font-size: clamp(35px, 7vw, 66px);
    line-height: .95;
    letter-spacing: -2px;
    margin: 16px 0;
    text-shadow: 0 0 40px #65f7ff25;
}

h1 span { color: var(--cyan); }

.description {
    color: #a7b1cc;
    font-size: 13px;
    line-height: 1.8;
}

button {
    margin-top: 22px;
    padding: 14px 30px;
    background: var(--cyan);
    color: #07101b;
    border: 0;
    border-radius: 5px;
    font-weight: 900;
    font-size: 12px;
    letter-spacing: 2px;
    cursor: pointer;
    box-shadow: 0 0 25px #65f7ff35;
    transition: transform .2s, box-shadow .2s;
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 35px #65f7ff70;
}

.footer {
    display: flex;
    justify-content: space-between;
    gap: 14px;
    flex-wrap: wrap;
    padding: 17px 3px 0;
    color: #8792b2;
    font-size: 11px;
    letter-spacing: 1px;
}

kbd {
    color: #e6edff;
    background: #1b2340;
    border: 1px solid #34405f;
    border-radius: 4px;
    padding: 4px 7px;
    margin: 0 3px;
}

@media(max-width: 550px) {
    body { padding: 12px; }
    .brand { letter-spacing: 2px; }
    .subtitle { letter-spacing: 1px; }
    .status { font-size: 9px; padding: 8px; }
    .hud { top: 12px; left: 13px; right: 13px; }
    .score { font-size: 20px; }
    .best .score { font-size: 16px; }
    .footer { font-size: 9px; }
}
</style>
</head>

<body>
<main class="game-shell">

    <header class="topbar">
        <div>
            <div class="brand">N // NEON RUNNER</div>
            <div class="subtitle">DINO SURVIVAL PROTOCOL</div>
        </div>
        <div class="status">● SYSTEM ONLINE</div>
    </header>

    <section class="game-card">

        <div class="hud">
            <div>
                <div class="hud-label">DISTANCE / SCORE</div>
                <div class="score" id="score">00000</div>
            </div>
            <div class="best">
                <div class="hud-label">PERSONAL BEST</div>
                <div class="score" id="best">00000</div>
            </div>
        </div>

        <canvas id="game" width="1000" height="440"
                aria-label="Dinosaur running game"></canvas>

        <div class="overlay" id="overlay">
            <div class="panel">
                <div class="eyebrow" id="eyebrow">MISSION 001 / SURVIVAL</div>
                <h1 id="heading">RUN INTO<br><span>THE NIGHT.</span></h1>
                <p class="description" id="description">
                    The world has gone dark. The run never ends.
                    Jump over obstacles and beat your distance record.
                </p>
                <button id="start">INITIALIZE RUN ↗</button>
            </div>
        </div>

    </section>

    <footer class="footer">
        <div><kbd>SPACE</kbd> <kbd>↑</kbd> JUMP</div>
        <div>DOUBLE TAP NOT REQUIRED · PRESS TO RESTART</div>
        <div>BUILD 01.0</div>
    </footer>

</main>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const W = 1000, H = 440, ground = 355;
const scoreEl = document.getElementById("score");
const bestEl = document.getElementById("best");
const overlay = document.getElementById("overlay");
const startBtn = document.getElementById("start");
const heading = document.getElementById("heading");
const eyebrow = document.getElementById("eyebrow");
const description = document.getElementById("description");

let running = false, dead = false;
let score = 0, best = 0, speed = 6;
let lastTime = 0, spawnTimer = 0, frame = 0;
let obstacles = [], particles = [];
let stars = [], mountains = [];
let groundOffset = 0, shake = 0;

try {
    best = Number(localStorage.getItem("neonDinoBest")) || 0;
} catch(e) {}
bestEl.textContent = String(best).padStart(5, "0");

for (let i = 0; i < 100; i++) {
    stars.push({
        x: Math.random() * W,
        y: Math.random() * 300,
        r: Math.random() * 1.7 + .3,
        a: Math.random() * .65 + .2,
        phase: Math.random() * 7
    });
}

for (let i = 0; i < 16; i++) {
    mountains.push({
        x: i * 100 - 30,
        h: 35 + Math.random() * 100,
        w: 90 + Math.random() * 100
    });
}

const dino = {
    x: 115, y: ground - 58, w: 48, h: 58,
    vy: 0, jumping: false, leg: 0
};

function rect(x, y, w, h, color) {
    ctx.fillStyle = color;
    ctx.fillRect(x, y, w, h);
}

function roundedRect(x, y, w, h, r, color) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.roundRect(x, y, w, h, r);
    ctx.fill();
}

function glow(color, blur) {
    ctx.shadowColor = color;
    ctx.shadowBlur = blur;
}

function background(dt) {
    const sky = ctx.createLinearGradient(0, 0, 0, H);
    sky.addColorStop(0, "#080d23");
    sky.addColorStop(.60, "#171b3c");
    sky.addColorStop(1, "#301c3a");
    rect(0, 0, W, H, sky);

    // Cinematic moon
    glow("#a3c9ff", 35);
    ctx.fillStyle = "#c7e3ff";
    ctx.beginPath();
    ctx.arc(780, 115, 37, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowBlur = 0;

    ctx.fillStyle = "#a5bbdf";
    ctx.globalAlpha = .45;
    ctx.beginPath();
    ctx.arc(768, 104, 7, 0, Math.PI * 2);
    ctx.arc(792, 128, 5, 0, Math.PI * 2);
    ctx.fill();
    ctx.globalAlpha = 1;

    // Stars
    for (const s of stars) {
        const twinkle = .65 + Math.sin(frame * .025 + s.phase) * .3;
        ctx.globalAlpha = s.a * twinkle;
        rect(s.x, s.y, s.r, s.r, "#e1edff");
    }
    ctx.globalAlpha = 1;

    // Distant city
    rect(0, 258, W, 100, "#10152e");
    for (let i = 0; i < 36; i++) {
        const x = i * 31;
        const bh = 20 + (Math.sin(i * 12.7) + 1) * 25;
        rect(x, 320 - bh, 23, bh + 40, "#121a35");

        for (let j = 0; j < 3; j++) {
            if ((i + j) % 3 !== 0) {
                ctx.globalAlpha = .45;
                rect(x + 5 + j * 6, 327 - bh, 2, 4, "#69bdf0");
            }
        }
    }
    ctx.globalAlpha = 1;

    // Layered mountains
    for (let layer = 0; layer < 2; layer++) {
        ctx.fillStyle = layer === 0 ? "#211b3d" : "#30203e";
        ctx.beginPath();
        ctx.moveTo(0, ground);
        for (let x = 0; x <= W; x += 25) {
            const wave = Math.sin(x * .012 + layer) * 19
                       + Math.sin(x * .027) * 11;
            ctx.lineTo(x, 295 + wave + layer * 17);
        }
        ctx.lineTo(W, ground);
        ctx.closePath();
        ctx.fill();
    }

    // Ground
    const dirt = ctx.createLinearGradient(0, ground, 0, H);
    dirt.addColorStop(0, "#201a36");
    dirt.addColorStop(1, "#080a18");
    rect(0, ground, W, H - ground, dirt);

    // Neon horizon
    glow("#ff855d", 17);
    rect(0, ground, W, 2, "#ff9b70");
    ctx.shadowBlur = 0;

    groundOffset = (groundOffset + speed * dt * .055) % 70;
    for (let x = -70; x < W + 70; x += 70) {
        const px = x - groundOffset;
        rect(px, ground + 24, 34, 2, "#49304e");
        rect(px + 17, ground + 40, 17, 1, "#344063");
    }

    // Vignette
    const v = ctx.createRadialGradient(W/2, H/2, 80, W/2, H/2, 650);
    v.addColorStop(0, "#00000000");
    v.addColorStop(1, "#02030caa");
    rect(0, 0, W, H, v);
}

function drawDino() {
    const x = dino.x, y = dino.y;
    const run = running && !dino.jumping ? Math.sin(dino.leg) : 0;

    ctx.save();
    glow("#65f7ff", 16);

    // Tail
    ctx.fillStyle = "#65f7ff";
    ctx.beginPath();
    ctx.moveTo(x + 7, y + 31);
    ctx.lineTo(x - 10, y + 39);
    ctx.lineTo(x + 8, y + 43);
    ctx.closePath();
    ctx.fill();

    // Body and neck
    roundedRect(x + 6, y + 20, 30, 26, 7, "#65f7ff");
    roundedRect(x + 24, y + 4, 17, 27, 5, "#65f7ff");

    // Head
    roundedRect(x + 20, y, 31, 24, 5, "#91ffff");
    rect(x + 38, y + 8, 5, 5, "#081022");
    rect(x + 44, y + 17, 9, 3, "#152543");

    // Small back spikes
    ctx.fillStyle = "#65f7ff";
    for (let i = 0; i < 3; i++) {
        ctx.beginPath();
        ctx.moveTo(x + 10 + i * 8, y + 20);
        ctx.lineTo(x + 14 + i * 8, y + 12);
        ctx.lineTo(x + 19 + i * 8, y + 20);
        ctx.fill();
    }

    ctx.shadowBlur = 0;

    // Legs
    const legA = run * 7;
    rect(x + 11, y + 42, 8, 11 + legA, "#65f7ff");
    rect(x + 28, y + 42, 8, 11 - legA, "#65f7ff");
    rect(x + 7, y + 54 + legA, 14, 4, "#91ffff");
    rect(x + 25, y + 54 - legA, 14, 4, "#91ffff");

    ctx.restore();
}

function cactus(x, y, w, h) {
    ctx.save();
    glow("#ff805f", 12);
    roundedRect(x + w * .3, y, w * .4, h, 5, "#ff9d72");
    roundedRect(x, y + h * .42, w * .35, h * .15, 4, "#ff9d72");
    roundedRect(x, y + h * .28, w * .18, h * .3, 4, "#ff9d72");
    roundedRect(x + w * .65, y + h * .56, w * .35, h * .14, 4, "#ff9d72");
    roundedRect(x + w * .82, y + h * .38, w * .18, h * .32, 4, "#ff9d72");
    ctx.shadowBlur = 0;
    ctx.restore();
}

function rock(x, y) {
    ctx.save();
    glow("#b58aff", 10);
    ctx.fillStyle = "#c09aff";
    ctx.beginPath();
    ctx.moveTo(x, y + 24);
    ctx.lineTo(x + 9, y + 7);
    ctx.lineTo(x + 23, y);
    ctx.lineTo(x + 35, y + 13);
    ctx.lineTo(x + 32, y + 24);
    ctx.closePath();
    ctx.fill();
    ctx.shadowBlur = 0;
    ctx.restore();
}

function burst(x, y, color) {
    for (let i = 0; i < 22; i++) {
        particles.push({
            x, y,
            vx: (Math.random() - .5) * 8,
            vy: (Math.random() - .7) * 8,
            life: 1,
            color
        });
    }
}

function drawParticles(dt) {
    for (const p of particles) {
        p.x += p.vx * dt * .06;
        p.y += p.vy * dt * .06;
        p.vy += .15 * dt;
        p.life -= .018 * dt;
        ctx.globalAlpha = Math.max(0, p.life);
        rect(p.x, p.y, 4, 4, p.color);
    }
    ctx.globalAlpha = 1;
    particles = particles.filter(p => p.life > 0);
}

function startGame() {
    score = 0;
    speed = 6;
    obstacles = [];
    particles = [];
    spawnTimer = 65;
    shake = 0;

    dino.y = ground - dino.h;
    dino.vy = 0;
    dino.jumping = false;

    running = true;
    dead = false;
    overlay.classList.add("hidden");
    lastTime = performance.now();
}

function jump() {
    if (!running) {
        if (dead) startGame();
        else startGame();
        return;
    }

    if (!dino.jumping) {
        dino.vy = -14.5;
        dino.jumping = true;
        burst(dino.x + 20, ground - 3, "#65f7ff");
    }
}

function gameOver() {
    running = false;
    dead = true;
    shake = 12;

    burst(dino.x + 25, dino.y + 25, "#ff795f");

    best = Math.max(best, Math.floor(score));
    try {
        localStorage.setItem("neonDinoBest", best);
    } catch(e) {}

    bestEl.textContent = String(best).padStart(5, "0");

    eyebrow.textContent = "MISSION FAILED / RETRY";
    heading.innerHTML = "THE NIGHT<br><span>WINS.</span>";
    description.textContent =
        "Distance covered: " + Math.floor(score) +
        ". Your record is " + best + ". The next run starts now.";
    startBtn.textContent = "RESTART MISSION ↗";
    overlay.classList.remove("hidden");
}

function update(dt) {
    frame += dt;

    if (running) {
        score += dt * speed * .11;
        speed = Math.min(13, 6 + score / 220);

        dino.vy += .72 * dt;
        dino.y += dino.vy * dt;

        if (dino.y >= ground - dino.h) {
            dino.y = ground - dino.h;
            dino.vy = 0;
            dino.jumping = false;
        }

        dino.leg += .25 * dt;

        spawnTimer -= dt;
        if (spawnTimer <= 0) {
            const h = 35 + Math.random() * 30;
            const isRock = Math.random() > .6;
            obstacles.push({
                x: W + 30,
                y: ground - h,
                w: isRock ? 36 : 44,
                h,
                type: isRock ? "rock" : "cactus"
            });
            spawnTimer = 75 + Math.random() * 60;
        }

        for (const o of obstacles) {
            o.x -= speed * dt;

            // Forgiving collision box for fair gameplay
            const ax = dino.x + 9, ay = dino.y + 8;
            const aw = dino.w - 17, ah = dino.h - 12;
            const bx = o.x + 5, by = o.y + 4;
            const bw = o.w - 10, bh = o.h - 4;

            if (ax < bx + bw && ax + aw > bx &&
                ay < by + bh && ay + ah > by) {
                gameOver();
                break;
            }
        }

        obstacles = obstacles.filter(o => o.x > -100);
        scoreEl.textContent = String(Math.floor(score)).padStart(5, "0");
    }

    drawParticles(dt);
}

function render(now) {
    const dt = Math.min((now - (lastTime || now)) / 16.67, 2);
    lastTime = now;

    ctx.save();

    if (shake > 0) {
        ctx.translate(
            (Math.random() - .5) * shake,
            (Math.random() - .5) * shake
        );
        shake *= .85;
        if (shake < .4) shake = 0;
    }

    background(dt);

    for (const o of obstacles) {
        if (o.type === "rock") rock(o.x, o.y);
        else cactus(o.x, o.y, o.w, o.h);
    }

    if (running || !dead) drawDino();

    update(dt);
    ctx.restore();

    requestAnimationFrame(render);
}

startBtn.addEventListener("click", startGame);
canvas.addEventListener("pointerdown", jump);

document.addEventListener("keydown", e => {
    if (["Space", "ArrowUp", "KeyW"].includes(e.code)) {
        e.preventDefault();
        if (!e.repeat) jump();
    }
    if (e.code === "Enter" && !running) startGame();
});

requestAnimationFrame(render);
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
