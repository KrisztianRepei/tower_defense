**Repei Krisztián (RK) | QDDSEJ**
-

**Feladat leírása**
-

A projektben egy egyszerű Tower Defense játékot készítettem Pythonban. A feladat előírása szerint minden modulban, osztályban és függvényben szerepel a saját monogramom (RK). A játékban tornyokat lehet lerakni, amelyek automatikusan lövik az útvonalon haladó ellenfeleket. A rendszer hullámokra épül, a cél pedig az, hogy a játékos túlélje az összeset.

**settings_RK.py**
-
- Nincsenek függvények, csak konstansok / beállítások.

**utils_RK.py | Függvények:**
-
- dist_RK(a, b)
- clamp_RK(v, lo, hi)
- lerp_RK(a, b, t)

**entities_RK.py | Osztályok és metódusok:**
-
- EnemyRK ( update_RK(dt), take_damage_RK(dmg), draw_RK(screen) )
- ProjectileRK ( update_RK(dt), draw_RK(screen) )
- TowerRK ( update_RK(dt, enemies, projectiles), draw_RK(screen) )

**waves_RK.py | Osztályok és metódusok:**
-
- WaveManagerRK ( start_next_wave_RK(), update_RK(dt, enemies) )

**ui_RK.py | Osztályok és metódusok:**
-
- UIButtonRK ( handle_event_RK(event), draw_RK(screen, font) )
- UIOverlayRK ( draw_hud_RK(screen, gold, lives, wave_idx, wave_active, finished), draw_message_center_RK(screen, msg), draw_hint_RK(screen, msg) )

**main_RK.py | Függvények:**
-

- snap_to_grid_RK(pos)
- is_on_path_RK(pos, path_points, threshold=25)
- main_RK()

**Belső (mainen belüli) függvény:**
-
- start_wave_RK() (belső callback a gombhoz)

**Összes osztály egybe:**
- 
- EnemyRK
- ProjectileRK
- TowerRK
- WaveManagerRK
- UIButtonRK
- UIOverlayRK

