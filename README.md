# Space Invaders — Unity-inspired Python/Pygame

🇺🇸 English | [🇧🇷 Português](#-português-pt-br)

A fully playable **Space Invaders clone** built with Python + [pygame-ce](https://pyga.me/),
structured to mirror the **Unity/C# component architecture** as closely as Python allows.
The codebase serves as a structural reference for a future Unity project: GameObjects,
MonoBehaviour lifecycle, Scenes, prefab factories, a static `Time`/`Input`/`Physics2D` API —
everything maps 1:1 to a Unity concept.

All sprites are drawn procedurally from pixel grids and all sounds are synthesized
at startup (square waves / noise) — **no external asset files required**. Drop `.ttf`
files into `assets/fonts/` or `.wav` files into `assets/sounds/` to override them.

## Architecture

```text
┌─────────────────────────────────────────────────────────┐
│ main.py            bootstraps GameEngine + first Scene  │
├─────────────────────────────────────────────────────────┤
│ scenes/            MenuScene · GameScene · GameOverScene│
│ prefabs/           factory functions -> GameObjects     │
│ scripts/           game-specific MonoBehaviours         │
├─────────────────────────────────────────────────────────┤
│ components/        Transform · SpriteRenderer ·         │
│                    BoxCollider2D (engine-level)         │
├─────────────────────────────────────────────────────────┤
│ core/  (no game logic)                                  │
│   GameEngine    main loop (Unity runtime)               │
│   GameObject    component container                     │
│   MonoBehaviour lifecycle protocol                      │
│   Scene / SceneManager                                  │
│   Time · Input · Physics2D (static classes)             │
└─────────────────────────────────────────────────────────┘
```

### Unity mapping

| Python | Unity equivalent |
| ------ | ---------------- |
| `MonoBehaviour` | `MonoBehaviour` |
| `game_object` | `gameObject` |
| `Time.delta_time` | `Time.deltaTime` |
| `get_component(Type)` | `GetComponent<T>()` |
| `scene.find_object_of_type(Type)` | `FindObjectOfType<T>()` |
| `scene.instantiate(go)` | `Instantiate(prefab)` |
| `scene.destroy(go)` / `go.destroy()` | `Destroy(go)` |
| `awake()` / `start()` / `update(dt)` / `on_destroy()` | `Awake()` / `Start()` / `Update()` / `OnDestroy()` |
| `on_trigger_enter_2d(other)` | `OnTriggerEnter2D(Collider2D)` |
| `prefabs/create_player(scene)` | prefab asset + `Instantiate` |
| `SceneManager.load_scene(scene)` | `SceneManager.LoadScene()` |

### Frame order (mirrors Unity execution order)

1. Apply pending scene transition
2. `Input.update()`
3. `Time.tick()`
4. `Physics2D.check_all_overlaps()`
5. `scene.update(dt)`
6. Render sorted by `layer_order`
7. Flush destroyed objects (also unregisters colliders)

## Setup

Requires Python 3.12+ and [Poetry](https://python-poetry.org/).

```bash
poetry install
poetry run space-invaders
```

Run the tests:

```bash
poetry run pytest
```

## Controls

| Key | Action |
| --- | ------ |
| ← → | Move ship |
| SPACE | Shoot (one bullet at a time, 0.5 s cooldown) |
| P | Pause (`Time.time_scale = 0`) |
| ENTER | Start / retry |
| ESC | Back to menu (in game) / quit (in menus) |

## Game rules

- 5 × 11 invader formation marches sideways, drops and reverses at the edges, and
  speeds up as invaders die and waves advance.
- Invaders: bottom rows = 10 pts, middle = 20 pts, top = 30 pts. Bonus UFO crosses
  the top every ~25 s for a random 50–300 pts.
- 4 destructible barriers erode cell by cell where bullets hit.
- Clear the wave → next wave, faster. Lose all 3 lives or let the invaders reach
  your row → game over.

## Project structure

```text
space-invaders-clone/
├── assets/fonts, assets/sounds   # optional overrides (.ttf / .wav)
├── src/space_invaders/
│   ├── main.py · settings.py
│   ├── core/         engine layer
│   ├── components/   Transform, SpriteRenderer, BoxCollider2D
│   ├── scripts/      player, bullets, invaders, formation, UFO,
│   │                 barriers, GameManager, UIManager, AudioManager
│   ├── scenes/       menu, game, game over
│   ├── prefabs/      GameObject factory functions
│   └── utils/        pixel-sprite and text helpers
└── tests/            core-layer unit tests (no rendering needed)
```

---

## 🇧🇷 Português (PT-BR)

Um clone **totalmente jogável de Space Invaders** feito em Python + [pygame-ce](https://pyga.me/),
estruturado para espelhar a **arquitetura de componentes do Unity/C#** o máximo que o
Python permite. O código serve como referência estrutural para um futuro projeto em
Unity: GameObjects, ciclo de vida MonoBehaviour, Scenes, fábricas de prefabs e as
classes estáticas `Time`/`Input`/`Physics2D` — tudo tem correspondência 1:1 com o Unity
(veja a tabela de mapeamento acima).

Todos os sprites são desenhados proceduralmente a partir de grades de pixels e todos
os sons são sintetizados na inicialização — **nenhum arquivo de asset é necessário**.
Coloque arquivos `.ttf` em `assets/fonts/` ou `.wav` em `assets/sounds/` para substituí-los.

### Instalação

Requer Python 3.12+ e [Poetry](https://python-poetry.org/).

```bash
poetry install
poetry run space-invaders
```

Rodar os testes:

```bash
poetry run pytest
```

### Controles

| Tecla | Ação |
| ----- | ---- |
| ← → | Move a nave |
| ESPAÇO | Atira (uma bala por vez, cooldown de 0,5 s) |
| P | Pausa (`Time.time_scale = 0`) |
| ENTER | Iniciar / tentar de novo |
| ESC | Voltar ao menu (no jogo) / sair (nos menus) |

### Regras

- Formação de 5 × 11 invasores marcha lateralmente, desce e inverte nas bordas, e
  acelera conforme invasores morrem e as ondas avançam.
- Invasores: fileiras de baixo = 10 pts, meio = 20 pts, topo = 30 pts. O UFO bônus
  cruza o topo a cada ~25 s valendo 50–300 pts aleatórios.
- 4 barreiras destrutíveis erodem célula a célula onde as balas acertam.
- Limpou a onda → próxima onda, mais rápida. Perdeu as 3 vidas ou deixou os
  invasores chegarem à sua linha → game over.

### Ordem do frame (espelha a ordem de execução do Unity)

1. Aplica transição de cena pendente
2. `Input.update()`
3. `Time.tick()`
4. `Physics2D.check_all_overlaps()`
5. `scene.update(dt)`
6. Renderização ordenada por `layer_order`
7. Remoção dos objetos destruídos no fim do frame
