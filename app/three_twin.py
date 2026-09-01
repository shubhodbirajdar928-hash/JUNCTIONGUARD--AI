"""
JunctionGuard AI - 3D Digital Twin WebGL Component
Renders an interactive Three.js 3D urban road junction with:
  - Dynamic mixed traffic (Cars, Two-Wheelers, Buses, Trucks)
  - Animated traffic signal towers with dynamic phase cycling
  - Dynamic risk ground beacon bound to real-time risk scores
  - 3 Interactive Camera Presets (Tactical 3D, Overhead Radar, Street Cam)
  - Resilient WebGL auto-resizing with ResizeObserver
"""

import streamlit.components.v1 as components

def render_3d_junction_digital_twin(
    junction_name: str = "Silk Board Junction",
    risk_score: float = 69.7,
    risk_level: str = "MEDIUM",
    city: str = "Bengaluru",
    total_vehicles: int = 42,
    two_wheeler_pct: float = 48.0,
    pedestrians: int = 14,
    height: int = 460
):
    """
    Renders an interactive Three.js 3D Digital Twin visualization in Streamlit.
    """
    score_val = max(0.0, min(100.0, float(risk_score or 0.0)))
    level_upper = (risk_level or "LOW").upper()
    
    if level_upper == "HIGH":
        beacon_color = "#f43f5e"
        beacon_rgb = "244, 63, 94"
        traffic_speed = 1.35
    elif level_upper == "MEDIUM":
        beacon_color = "#f59e0b"
        beacon_rgb = "245, 158, 11"
        traffic_speed = 1.0
    else:
        beacon_color = "#10b981"
        beacon_rgb = "16, 185, 129"
        traffic_speed = 0.8

    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>JunctionGuard 3D Digital Twin</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            html, body {{
                width: 100%;
                height: 100%;
                overflow: hidden;
                background-color: #050811;
                font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                color: #f1f5f9;
                user-select: none;
            }}
            #canvas-container {{
                width: 100%;
                height: {height}px;
                position: relative;
                border-radius: 16px;
                overflow: hidden;
                border: 1px solid rgba(99, 102, 241, 0.35);
                box-shadow: 0 16px 40px rgba(0, 0, 0, 0.75), inset 0 0 30px rgba(99, 102, 241, 0.12);
                background: #050811;
            }}
            #three-canvas {{
                width: 100%;
                height: 100%;
                display: block;
            }}
            /* HUD Overlays */
            .hud-overlay {{
                position: absolute;
                pointer-events: none;
            }}
            .hud-top-left {{
                top: 12px;
                left: 14px;
                background: rgba(7, 10, 19, 0.88);
                backdrop-filter: blur(14px);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 12px;
                padding: 10px 14px;
                display: flex;
                flex-direction: column;
                gap: 4px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.5);
                z-index: 10;
            }}
            .hud-title {{
                font-size: 0.86rem;
                font-weight: 800;
                color: #ffffff;
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            .hud-badge {{
                font-size: 0.68rem;
                font-weight: 700;
                padding: 2px 8px;
                border-radius: 9999px;
                font-family: 'JetBrains Mono', monospace;
                background: rgba({beacon_rgb}, 0.2);
                color: {beacon_color};
                border: 1px solid rgba({beacon_rgb}, 0.45);
            }}
            .hud-meta {{
                font-size: 0.72rem;
                color: #94a3b8;
                font-family: 'JetBrains Mono', monospace;
            }}
            .hud-top-right {{
                top: 12px;
                right: 14px;
                display: flex;
                gap: 6px;
                pointer-events: auto;
                z-index: 10;
            }}
            .hud-btn {{
                background: rgba(15, 23, 42, 0.88);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.14);
                border-radius: 8px;
                padding: 6px 10px;
                font-size: 0.72rem;
                font-weight: 700;
                color: #cbd5e1;
                cursor: pointer;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                gap: 5px;
            }}
            .hud-btn:hover {{
                background: #1e293b;
                color: #38bdf8;
                border-color: #38bdf8;
                transform: translateY(-1px);
            }}
            .hud-btn.active {{
                background: rgba(56, 189, 248, 0.2);
                color: #38bdf8;
                border-color: #38bdf8;
            }}
            .hud-bottom {{
                bottom: 10px;
                left: 14px;
                right: 14px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: rgba(7, 10, 19, 0.85);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 8px 14px;
                font-size: 0.70rem;
                font-family: 'JetBrains Mono', monospace;
                z-index: 10;
            }}
            .hud-stat-item {{
                display: flex;
                align-items: center;
                gap: 6px;
                color: #94a3b8;
            }}
            .hud-stat-val {{
                color: #ffffff;
                font-weight: 700;
            }}
            .live-dot {{
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background: #10b981;
                box-shadow: 0 0 8px #10b981;
                display: inline-block;
                animation: blink 1.8s infinite;
            }}
            @keyframes blink {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.3; }}
            }}
        </style>
        <!-- Robust Three.js CDN -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    </head>
    <body>
        <div id="canvas-container">
            <div class="hud-overlay hud-top-left">
                <div class="hud-title">
                    <span>3D DIGITAL TWIN</span>
                    <span class="hud-badge">{level_upper} · {score_val:.1f}/100</span>
                </div>
                <div class="hud-meta">📍 {junction_name}, {city}</div>
            </div>

            <div class="hud-top-right">
                <button class="hud-btn active" id="btn-rotate">🔄 Orbit</button>
                <button class="hud-btn" id="btn-view-tactical">🛰️ Tactical</button>
                <button class="hud-btn" id="btn-view-top">🚁 Overhead</button>
                <button class="hud-btn" id="btn-view-street">🛣️ Street</button>
                <button class="hud-btn" id="btn-reset">🎯 Reset</button>
            </div>

            <div class="hud-overlay hud-bottom">
                <div class="hud-stat-item"><span class="live-dot"></span> <span>STATUS:</span> <span class="hud-stat-val">LIVE TWIN</span></div>
                <div class="hud-stat-item"><span>FLOW DENSITY:</span> <span class="hud-stat-val">{total_vehicles} VEH/MIN</span></div>
                <div class="hud-stat-item"><span>2-WHEELER SHARE:</span> <span class="hud-stat-val">{two_wheeler_pct:.1f}%</span></div>
                <div class="hud-stat-item"><span>PEDESTRIAN RISK:</span> <span class="hud-stat-val">{pedestrians} ACTIVE</span></div>
                <div class="hud-stat-item" style="color:#6366f1;"><span>ENGINE:</span> <span class="hud-stat-val" style="color:#38bdf8;">WEBGL 3D</span></div>
            </div>

            <canvas id="three-canvas"></canvas>
        </div>

        <script>
            // ── Safe WebGL Canvas & Scene Initialization ──
            const container = document.getElementById('canvas-container');
            const canvas = document.getElementById('three-canvas');

            function getWidth() {{ return container.clientWidth || window.innerWidth || 800; }}
            function getHeight() {{ return container.clientHeight || {height}; }}

            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x050811);
            scene.fog = new THREE.FogExp2(0x050811, 0.015);

            const camera = new THREE.PerspectiveCamera(42, getWidth() / getHeight(), 0.1, 1000);
            camera.position.set(24, 28, 32);

            const renderer = new THREE.WebGLRenderer({{
                canvas: canvas,
                antialias: true,
                alpha: false,
                powerPreference: "high-performance"
            }});
            renderer.setSize(getWidth(), getHeight());
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;

            const controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.maxPolarAngle = Math.PI / 2.15;
            controls.minDistance = 10;
            controls.maxDistance = 85;
            controls.target.set(0, 0, 0);

            let autoRotate = true;

            // ── Lighting Setup ──
            const ambientLight = new THREE.AmbientLight(0x6366f1, 0.5);
            scene.add(ambientLight);

            const dirLight = new THREE.DirectionalLight(0xffffff, 0.9);
            dirLight.position.set(25, 45, 25);
            dirLight.castShadow = true;
            dirLight.shadow.mapSize.width = 1024;
            dirLight.shadow.mapSize.height = 1024;
            scene.add(dirLight);

            const cyanPointLight = new THREE.PointLight(0x38bdf8, 1.4, 45);
            cyanPointLight.position.set(-18, 14, -18);
            scene.add(cyanPointLight);

            const hazardLightColor = "{beacon_color}";
            const hazardPointLight = new THREE.PointLight(hazardLightColor, 2.2, 30);
            hazardPointLight.position.set(0, 4, 0);
            scene.add(hazardPointLight);

            // ── Ground & Grid ──
            const groundGeo = new THREE.PlaneGeometry(180, 180);
            const groundMat = new THREE.MeshStandardMaterial({{
                color: 0x080c18,
                roughness: 0.9,
                metalness: 0.2
            }});
            const ground = new THREE.Mesh(groundGeo, groundMat);
            ground.rotation.x = -Math.PI / 2;
            ground.receiveShadow = true;
            scene.add(ground);

            const gridHelper = new THREE.GridHelper(180, 90, 0x1e293b, 0x0f172a);
            gridHelper.position.y = 0.01;
            scene.add(gridHelper);

            // ── Road Geometry & Intersection ──
            const roadWidth = 11;
            const roadLength = 150;
            const roadMat = new THREE.MeshStandardMaterial({{ color: 0x0f1422, roughness: 0.7, metalness: 0.3 }});

            // North-South Road
            const nsRoadGeo = new THREE.PlaneGeometry(roadWidth, roadLength);
            const nsRoad = new THREE.Mesh(nsRoadGeo, roadMat);
            nsRoad.rotation.x = -Math.PI / 2;
            nsRoad.position.y = 0.02;
            nsRoad.receiveShadow = true;
            scene.add(nsRoad);

            // East-West Road
            const ewRoadGeo = new THREE.PlaneGeometry(roadLength, roadWidth);
            const ewRoad = new THREE.Mesh(ewRoadGeo, roadMat);
            ewRoad.rotation.x = -Math.PI / 2;
            ewRoad.position.y = 0.02;
            ewRoad.receiveShadow = true;
            scene.add(ewRoad);

            // Lane Divider Dashes
            const dashLineMat = new THREE.MeshBasicMaterial({{ color: 0xfacc15 }});
            for (let i = -roadLength / 2; i < roadLength / 2; i += 4) {{
                if (Math.abs(i) > roadWidth / 2 + 1) {{
                    const dashNS = new THREE.Mesh(new THREE.PlaneGeometry(0.3, 2), dashLineMat);
                    dashNS.rotation.x = -Math.PI / 2;
                    dashNS.position.set(0, 0.03, i);
                    scene.add(dashNS);

                    const dashEW = new THREE.Mesh(new THREE.PlaneGeometry(2, 0.3), dashLineMat);
                    dashEW.rotation.x = -Math.PI / 2;
                    dashEW.position.set(i, 0.03, 0);
                    scene.add(dashEW);
                }}
            }}

            // Pedestrian Crosswalks
            const crosswalkMat = new THREE.MeshBasicMaterial({{ color: 0xe2e8f0 }});
            const createCrosswalk = (x, z, isHorizontal) => {{
                for (let k = -roadWidth / 2 + 1.0; k <= roadWidth / 2 - 1.0; k += 1.3) {{
                    const stripe = new THREE.Mesh(
                        new THREE.PlaneGeometry(isHorizontal ? 2.5 : 0.6, isHorizontal ? 0.6 : 2.5),
                        crosswalkMat
                    );
                    stripe.rotation.x = -Math.PI / 2;
                    stripe.position.set(isHorizontal ? x : k, 0.035, isHorizontal ? k : z);
                    scene.add(stripe);
                }}
            }};
            createCrosswalk(0, roadWidth / 2 + 2, false);
            createCrosswalk(0, -roadWidth / 2 - 2, false);
            createCrosswalk(roadWidth / 2 + 2, 0, true);
            createCrosswalk(-roadWidth / 2 - 2, 0, true);

            // ── Dynamic Center Risk Beacon ──
            const ringGeo = new THREE.RingGeometry(roadWidth / 2 - 1.5, roadWidth / 2 + 1.0, 64);
            const ringMat = new THREE.MeshBasicMaterial({{
                color: new THREE.Color("{beacon_color}"),
                side: THREE.DoubleSide,
                transparent: true,
                opacity: 0.7
            }});
            const hazardRing = new THREE.Mesh(ringGeo, ringMat);
            hazardRing.rotation.x = -Math.PI / 2;
            hazardRing.position.y = 0.04;
            scene.add(hazardRing);

            // Volumetric Cylinder Pillar
            const cylinderGeo = new THREE.CylinderGeometry(roadWidth / 2, roadWidth / 2, 7, 32, 1, true);
            const cylinderMat = new THREE.MeshBasicMaterial({{
                color: new THREE.Color("{beacon_color}"),
                transparent: true,
                opacity: 0.16,
                side: THREE.DoubleSide
            }});
            const hazardCylinder = new THREE.Mesh(cylinderGeo, cylinderMat);
            hazardCylinder.position.set(0, 3.5, 0);
            scene.add(hazardCylinder);

            // ── Surrounding Cyber City Buildings ──
            const buildingMat = new THREE.MeshStandardMaterial({{
                color: 0x090e1c,
                roughness: 0.8,
                metalness: 0.5
            }});
            const edgeMat = new THREE.LineBasicMaterial({{ color: 0x1e293b }});

            const buildingPositions = [
                [-24, -24], [-40, -24], [-24, -40],
                [24, -24], [40, -24], [24, -40],
                [-24, 24], [-40, 24], [-24, 40],
                [24, 24], [40, 24], [24, 40]
            ];

            buildingPositions.forEach(([bx, bz]) => {{
                const height = 12 + Math.random() * 24;
                const width = 13 + Math.random() * 4;
                const bGeo = new THREE.BoxGeometry(width, height, width);
                const bMesh = new THREE.Mesh(bGeo, buildingMat);
                bMesh.position.set(bx, height / 2, bz);
                bMesh.castShadow = true;
                bMesh.receiveShadow = true;
                scene.add(bMesh);

                const edges = new THREE.EdgesGeometry(bGeo);
                const line = new THREE.LineSegments(edges, edgeMat);
                line.position.copy(bMesh.position);
                scene.add(line);
            }});

            // ── Animated Traffic Signal Towers with Phasing LED Bulbs ──
            const signalPositions = [
                [roadWidth / 2 + 1.4, roadWidth / 2 + 1.4],
                [-roadWidth / 2 - 1.4, roadWidth / 2 + 1.4],
                [roadWidth / 2 + 1.4, -roadWidth / 2 - 1.4],
                [-roadWidth / 2 - 1.4, -roadWidth / 2 - 1.4]
            ];
            const signalBulbs = [];

            signalPositions.forEach(([sx, sz]) => {{
                // Pole
                const poleGeo = new THREE.CylinderGeometry(0.18, 0.18, 6.5, 12);
                const poleMat = new THREE.MeshStandardMaterial({{ color: 0x334155, metalness: 0.8 }});
                const pole = new THREE.Mesh(poleGeo, poleMat);
                pole.position.set(sx, 3.25, sz);
                scene.add(pole);

                // Box
                const boxGeo = new THREE.BoxGeometry(0.6, 1.5, 0.6);
                const boxMat = new THREE.MeshStandardMaterial({{ color: 0x0f172a }});
                const box = new THREE.Mesh(boxGeo, boxMat);
                box.position.set(sx, 5.5, sz);
                scene.add(box);

                // Active Bulb
                const bulbGeo = new THREE.SphereGeometry(0.20, 16, 16);
                const bulbMat = new THREE.MeshBasicMaterial({{ color: new THREE.Color(0x10b981) }});
                const bulb = new THREE.Mesh(bulbGeo, bulbMat);
                bulb.position.set(sx, 5.5, sz + (sz > 0 ? 0.35 : -0.35));
                scene.add(bulb);
                signalBulbs.push(bulb);
            }});

            // ── Animated Traffic Vehicles (Cars, Two-Wheelers, Buses, Trucks) ──
            const vehicles = [];
            const vehicleTypes = [
                {{ name: 'car', color: 0x38bdf8, w: 1.6, h: 1.1, l: 3.2, speed: 0.19 * {traffic_speed} }},
                {{ name: 'bike', color: 0xfacc15, w: 0.7, h: 0.9, l: 1.6, speed: 0.25 * {traffic_speed} }},
                {{ name: 'car2', color: 0x10b981, w: 1.6, h: 1.1, l: 3.4, speed: 0.18 * {traffic_speed} }},
                {{ name: 'bus', color: 0x6366f1, w: 2.2, h: 2.1, l: 6.2, speed: 0.14 * {traffic_speed} }},
                {{ name: 'truck', color: 0xf97316, w: 2.3, h: 2.3, l: 5.8, speed: 0.13 * {traffic_speed} }}
            ];

            const spawnLanes = [
                {{ dir: 'N2S', x: -roadWidth / 4, startZ: -roadLength / 2, dx: 0, dz: 1, rotY: 0 }},
                {{ dir: 'S2N', x: roadWidth / 4, startZ: roadLength / 2, dx: 0, dz: -1, rotY: Math.PI }},
                {{ dir: 'W2E', startX: -roadLength / 2, z: roadWidth / 4, dx: 1, dz: 0, rotY: Math.PI / 2 }},
                {{ dir: 'E2W', startX: roadLength / 2, z: -roadWidth / 4, dx: -1, dz: 0, rotY: -Math.PI / 2 }}
            ];

            const createVehicleMesh = (type) => {{
                const group = new THREE.Group();
                const bodyGeo = new THREE.BoxGeometry(type.w, type.h, type.l);
                const bodyMat = new THREE.MeshStandardMaterial({{ color: type.color, roughness: 0.3, metalness: 0.7 }});
                const body = new THREE.Mesh(bodyGeo, bodyMat);
                body.position.y = type.h / 2 + 0.2;
                body.castShadow = true;
                group.add(body);

                // Headlights
                const lightGeo = new THREE.SphereGeometry(0.12, 8, 8);
                const lightMat = new THREE.MeshBasicMaterial({{ color: 0xffffff }});
                const l1 = new THREE.Mesh(lightGeo, lightMat);
                l1.position.set(-type.w / 3, type.h / 2 + 0.1, type.l / 2 + 0.05);
                const l2 = new THREE.Mesh(lightGeo, lightMat);
                l2.position.set(type.w / 3, type.h / 2 + 0.1, type.l / 2 + 0.05);
                group.add(l1, l2);

                // Taillights
                const tailMat = new THREE.MeshBasicMaterial({{ color: 0xf43f5e }});
                const t1 = new THREE.Mesh(lightGeo, tailMat);
                t1.position.set(-type.w / 3, type.h / 2 + 0.1, -type.l / 2 - 0.05);
                const t2 = new THREE.Mesh(lightGeo, tailMat);
                t2.position.set(type.w / 3, type.h / 2 + 0.1, -type.l / 2 - 0.05);
                group.add(t1, t2);

                return group;
            }};

            // Spawn 16 active vehicles along lanes
            for (let i = 0; i < 16; i++) {{
                const lane = spawnLanes[i % spawnLanes.length];
                const type = vehicleTypes[Math.floor(Math.random() * vehicleTypes.length)];
                const mesh = createVehicleMesh(type);

                let posX = lane.x !== undefined ? lane.x : lane.startX + (i * 18);
                let posZ = lane.z !== undefined ? lane.z : lane.startZ + (i * 18);

                mesh.position.set(posX, 0, posZ);
                mesh.rotation.y = lane.rotY;
                scene.add(mesh);

                vehicles.push({{
                    mesh: mesh,
                    lane: lane,
                    type: type,
                    speed: type.speed * (0.85 + Math.random() * 0.3)
                }});
            }}

            // ── Camera Preset Controls ──
            const btnRotate = document.getElementById('btn-rotate');
            btnRotate.addEventListener('click', () => {{
                autoRotate = !autoRotate;
                btnRotate.classList.toggle('active', autoRotate);
            }});

            document.getElementById('btn-view-tactical').addEventListener('click', () => {{
                autoRotate = false;
                btnRotate.classList.remove('active');
                camera.position.set(24, 28, 32);
                controls.target.set(0, 0, 0);
            }});

            document.getElementById('btn-view-top').addEventListener('click', () => {{
                autoRotate = false;
                btnRotate.classList.remove('active');
                camera.position.set(0, 52, 0.1);
                controls.target.set(0, 0, 0);
            }});

            document.getElementById('btn-view-street').addEventListener('click', () => {{
                autoRotate = false;
                btnRotate.classList.remove('active');
                camera.position.set(-14, 4, 18);
                controls.target.set(0, 2, 0);
            }});

            document.getElementById('btn-reset').addEventListener('click', () => {{
                camera.position.set(24, 28, 32);
                controls.target.set(0, 0, 0);
            }});

            // ── Animation Loop ──
            let clock = new THREE.Clock();

            function animate() {{
                requestAnimationFrame(animate);
                const elapsedTime = clock.getElapsedTime();

                // Auto Orbit Rotation
                controls.autoRotate = autoRotate;
                controls.autoRotateSpeed = 1.0;
                controls.update();

                // Dynamic Pulsing Hazard Ground Ring & Light
                const pulseScale = 1.0 + Math.sin(elapsedTime * 3.5) * 0.12;
                hazardRing.scale.set(pulseScale, pulseScale, 1.0);
                hazardRing.material.opacity = 0.5 + Math.sin(elapsedTime * 3.5) * 0.3;
                hazardCylinder.material.opacity = 0.12 + Math.sin(elapsedTime * 3.5) * 0.08;
                hazardPointLight.intensity = 1.8 + Math.sin(elapsedTime * 3.5) * 0.8;

                // Signal Light Cycling (Green -> Amber -> Red every 6 seconds)
                const signalPhase = Math.floor(elapsedTime / 5) % 3;
                const signalColor = signalPhase === 0 ? 0x10b981 : (signalPhase === 1 ? 0xf59e0b : 0xf43f5e);
                signalBulbs.forEach(bulb => {{
                    bulb.material.color.setHex(signalColor);
                }});

                // Move Vehicles along lanes
                vehicles.forEach(v => {{
                    if (v.lane.dx !== 0) {{
                        v.mesh.position.x += v.lane.dx * v.speed;
                        if (v.lane.dx > 0 && v.mesh.position.x > roadLength / 2) {{
                            v.mesh.position.x = -roadLength / 2;
                        }} else if (v.lane.dx < 0 && v.mesh.position.x < -roadLength / 2) {{
                            v.mesh.position.x = roadLength / 2;
                        }}
                    }} else if (v.lane.dz !== 0) {{
                        v.mesh.position.z += v.lane.dz * v.speed;
                        if (v.lane.dz > 0 && v.mesh.position.z > roadLength / 2) {{
                            v.mesh.position.z = -roadLength / 2;
                        }} else if (v.lane.dz < 0 && v.mesh.position.z < -roadLength / 2) {{
                            v.mesh.position.z = roadLength / 2;
                        }}
                    }}
                }});

                renderer.render(scene, camera);
            }}
            animate();

            // ── Resilient Resize Observer ──
            const resizeObserver = new ResizeObserver(() => {{
                const w = getWidth();
                const h = getHeight();
                if (w > 0 && h > 0) {{
                    camera.aspect = w / h;
                    camera.updateProjectionMatrix();
                    renderer.setSize(w, h);
                }}
            }});
            resizeObserver.observe(container);
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=height + 20)
