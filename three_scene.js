/* ==========================================================================
   PRANAV'S RAMEN & CODE — THREE.JS 3D SCENE (three_scene.js)
   Loads enderh3art/Ramen-Shop original ramenShop.gltf with baked PNG textures.
   Camera positions ported directly from original Camera.js.
   ========================================================================== */

const originalLog = console.log;
const logBuffer = [];
console.log = function(...args) {
  originalLog.apply(console, args);
  logBuffer.push(args.join(' '));
};

function sendLogsToServer() {
  fetch('/', {
    method: 'POST',
    body: logBuffer.join('\n')
  }).catch(err => originalLog('Failed to send logs to server:', err));
}

let scene, camera, renderer, controls;
let raycaster, _mouse;
let modelLoaded = false;
let signHitBoxes = [];

// Camera coordinates from enderh3art Camera.js
const CAM = {
  default:  { pos: { x: -11.1, y: -1.0, z: -7.6 }, target: { x: 0,    y: 0,    z: -1  } },
  projects: { pos: { x:  1.15, y: -1.2, z:  4.2  }, target: { x: 1.15, y: -1.2, z: 1.7 } },
  aboutme:  { pos: { x:  0.66, y:  3.8, z:  2.2  }, target: { x: 0.66, y: 3.8,  z: 0.7 } },
  credits:  { pos: { x: -0.6,  y: -1.05,z:  3.8  }, target: { x: -0.6, y:-1.05, z: 2.2 } },
  skills:   { pos: { x: -0.6,  y: -1.05,z:  3.8  }, target: { x: -0.6, y:-1.05, z: 2.2 } },
  education:{ pos: { x:-10.2,  y:  6.3, z:  3.8  }, target: { x: 0,    y: 0,    z: -1  } },
  pranavs:  { pos: { x:  0.66, y:  3.8, z:  2.2  }, target: { x: 0.66, y: 3.8,  z: 0.7 } },
};

window.initThreeScene = function() {
  const canvas = document.querySelector('canvas.webgl');
  if (!canvas) { console.error('[3D] No canvas found'); return; }

  // Scene
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x000000);

  // Camera — matches original PerspectiveCamera(75, ..., 0.4, 50)
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.4, 50);
  camera.position.set(15.9, 6.8, -11.4); // opening position from Camera.js
  scene.add(camera);

  // Renderer
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.outputEncoding = THREE.sRGBEncoding;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.2;

  // OrbitControls — disabled until camera lands at default
  controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.enablePan = false;
  controls.rotateSpeed = 1.2;
  controls.zoomSpeed = 0.8;
  controls.target.set(0, 0, -1);
  controls.enableRotate = false;
  controls.enableZoom = false;
  controls.minDistance = 7;
  controls.maxDistance = 16;
  controls.minPolarAngle = Math.PI * 0.2;
  controls.maxPolarAngle = Math.PI * 0.55;

  // Raycaster
  raycaster = new THREE.Raycaster();
  _mouse = new THREE.Vector2();

  // Tiny ambient light (model is baked)
  scene.add(new THREE.AmbientLight(0xffffff, 0.04));

  // Invisible sign hitboxes
  buildSignHitBoxes();

  // Load model
  loadRamenShop();

  // Event listeners
  window.addEventListener('resize',    onResize);
  window.addEventListener('mousemove', onMouseMove);
  window.addEventListener('click',     onMouseClick);

  // Render loop
  animate();
};

/* --------------------------------------------------------------------------
   LOAD GLTF + BAKED PNG TEXTURES
   -------------------------------------------------------------------------- */
function loadRamenShop() {
  const loader  = new THREE.GLTFLoader();
  const dracoLoader = new THREE.DRACOLoader();
  dracoLoader.setDecoderPath('assets/draco/');
  loader.setDRACOLoader(dracoLoader);
  const texLoad = new THREE.TextureLoader();

  const cacheBuster = Date.now();
  function tex(file) {
    const t = texLoad.load('assets/textures/baked/' + file + '?v=' + cacheBuster);
    t.flipY    = false;
    t.encoding = THREE.sRGBEncoding;
    return t;
  }

  // Baked texture materials
  const baked = {
    ramenShop: new THREE.MeshBasicMaterial({ map: tex('ramenShopBaked1024.jpg') }),
    machines:  new THREE.MeshBasicMaterial({ map: tex('machinesBaked1024.jpg')  }),
    floor:     new THREE.MeshBasicMaterial({ map: tex('floorBaked1024.jpg')     }),
    misc:      new THREE.MeshBasicMaterial({ map: tex('miscBaked1024.jpg')      }),
    graphics:  new THREE.MeshBasicMaterial({ map: tex('graphicsBaked512.jpg')  }),
  };

  // Flat colour materials (from original Materials.mapColors())
  const col = (hex) => new THREE.MeshBasicMaterial({ color: hex });
  const flat = {
    white:     col('#FFFFFF'), black:  col('#000000'),
    pink:      col('#FF2FD5'), blue:   col('#01DDFF'),
    orange:    col('#FF5100'), red:    col('#FF0033'),
    green:     col('#1EFF51'),
    neonYellow:col('#FFF668'), neonPink: col('#FF3DCB'),
    neonBlue:  col('#00BBFF'), neonGreen:col('#56FF54'),
    redLed:    col('#FF112B'), greenLed: col('#00FF00'),
    screenOff: col('#030310'),
  };

  loader.load(
    'assets/models/ramenShop/glTF/ramenShop.gltf?v=' + cacheBuster,
    (gltf) => {
      const model = gltf.scene;
      model.position.y = -3;

      model.traverse((child) => {
        const n = child.name;

        // === MAIN SIGN: hide "Jesse's Ramen" 3D text geometry and glows entirely ===
        if (n && (n.toLowerCase().includes('jesse') || n.toLowerCase().includes('jzhou') || n.toLowerCase().includes('zhou'))) {
          console.log('[3D Meshes] HIDING Jesse Zhou object:', n);
          child.visible = false;
          return;
        }

        if (!child.isMesh) return;
        
        // Compute world bounding box for spatial search of the roof sign
        child.geometry.computeBoundingBox();
        const bbox = child.geometry.boundingBox.clone();
        child.updateMatrixWorld(true);
        bbox.applyMatrix4(child.matrixWorld);
        const center = new THREE.Vector3();
        bbox.getCenter(center);
        
        console.log('[DEBUG CENTER]: name =', n, 'center =', center.x.toFixed(2), center.y.toFixed(2), center.z.toFixed(2));

        console.log('[DEBUG SCENE MESH]: name =', n, 'material =', child.material ? child.material.type : 'none', 'visible =', child.visible);

        // Baked groups
        if      (n === 'ramenShopJoined') child.material = baked.ramenShop;
        else if (n === 'machinesJoined')  child.material = baked.machines;
        else if (n === 'floor')           child.material = baked.floor;
        else if (n === 'miscJoined')      child.material = baked.misc;
        else if (n === 'graphicsJoined')  child.material = baked.graphics;

        // Sign colours
        else if (n === 'projectsRed'  || n === 'articlesRed')   child.material = flat.red;
        else if (n === 'projectsWhite'|| n === 'articlesWhite') child.material = flat.white;
        else if (n === 'aboutMeBlack' || n === 'creditsBlack') child.material = flat.black;
        else if (n === 'aboutMeBlue'  || n === 'blueLights')    child.material = flat.blue;
        else if (n === 'creditsOrange'|| n === 'yellowRightLight') child.material = flat.orange;
        else if (n === 'greenSignSquare')   child.material = flat.green;
        else if (n === 'whiteButton')       child.material = flat.white;
        else if (n === 'redLED')            child.material = flat.redLed;
        else if (n === 'greenLED')          child.material = flat.greenLed;

        // Neon glow
        else if (n === 'chinese')           child.material = flat.neonGreen;
        else if (n === 'neonBlue' || n === 'portalLight' || n === 'storageLight' || n === 'poleLight' || n === 'lampLights' || n === 'arcadeRim') child.material = flat.neonBlue;
        else if (n === 'neonPink')          child.material = flat.neonPink;
        else if (n === 'neonYellow')        child.material = flat.neonYellow;
        else if (n === 'neonGreen')         child.material = flat.neonGreen;

        // Screens → dark placeholder
        else if (n.toLowerCase().includes('screen')) child.material = flat.screenOff;
      });

      scene.add(model);
      buildSignHitBoxes();
      modelLoaded = true;
      console.log('[3D] ramenShop.gltf loaded ✓');
      sendLogsToServer();
    },
    (xhr) => {
      if (xhr.total > 0) {
        const pct = Math.round((xhr.loaded / xhr.total) * 100);
        console.log(`[3D] Loading: ${pct}%`);
      }
    },
    (err) => {
      console.error('[3D] GLTF load error:', err);
    }
  );
}


/* --------------------------------------------------------------------------
   INVISIBLE SIGN HITBOXES — exact positions from RayCaster.js
   -------------------------------------------------------------------------- */
function buildSignHitBoxes() {
  const invisible = new THREE.MeshBasicMaterial({ visible: false });

  [
    { key: 'projects',  size: [0.4, 0.6,  1.7], pos: [-4,  0.4,   -5.0]  },
    { key: 'education', size: [0.4, 1.0,  1.0], pos: [-4, -0.4,  -4.72]  },
    { key: 'aboutme',   size: [0.4, 0.43, 1.7], pos: [-4, -1.83, -5.1]   },
    { key: 'credits',   size: [0.4, 0.4,  1.4], pos: [-4, -2.3,  -5.03]  },
  ].forEach(s => {
    const mesh = new THREE.Mesh(
      new THREE.BoxGeometry(...s.size),
      invisible.clone()
    );
    mesh.position.set(...s.pos);
    mesh.userData.sectionKey = s.key;
    scene.add(mesh);
    signHitBoxes.push(mesh);
  });
}

/* --------------------------------------------------------------------------
   CAMERA TRANSITIONS
   -------------------------------------------------------------------------- */
window.startCameraEntry = function() {
  tweenCamera(CAM.default, 2.5, () => {
    controls.enableRotate = true;
    controls.enableZoom   = true;
  });
};

window.focusCameraAndOpenModal = function(key) {
  const t = CAM[key] || CAM.default;
  controls.enableRotate = false;
  controls.enableZoom   = false;
  tweenCamera(t, 1.5, () => {
    controls.enableZoom = true;
    if (window.openModal) window.openModal(key);
  });
};

window.resetCameraToDefault = function() {
  controls.enableRotate = false;
  controls.enableZoom   = false;
  tweenCamera(CAM.default, 1.5, () => {
    controls.enableRotate = true;
    controls.enableZoom   = true;
  });
};

function tweenCamera(t, duration, onDone) {
  if (!window.gsap) {
    camera.position.set(t.pos.x, t.pos.y, t.pos.z);
    controls.target.set(t.target.x, t.target.y, t.target.z);
    controls.update();
    if (onDone) onDone();
    return;
  }
  gsap.to(camera.position, { x: t.pos.x, y: t.pos.y, z: t.pos.z, duration, ease: 'power2.inOut' });
  gsap.to(controls.target,  {
    x: t.target.x, y: t.target.y, z: t.target.z,
    duration, ease: 'power2.inOut',
    onUpdate: () => controls.update(),
    onComplete: onDone,
  });
}

/* --------------------------------------------------------------------------
   POINTER EVENTS
   -------------------------------------------------------------------------- */
function onMouseMove(e) {
  _mouse.x =  (e.clientX / window.innerWidth)  * 2 - 1;
  _mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

  if (!modelLoaded) return;

  raycaster.setFromCamera(_mouse, camera);
  const hits = raycaster.intersectObjects(signHitBoxes);
  document.body.style.cursor = hits.length > 0 ? 'pointer' : 'default';
}

function onMouseClick() {
  if (!modelLoaded) return;

  raycaster.setFromCamera(_mouse, camera);
  const hits = raycaster.intersectObjects(signHitBoxes);
  if (hits.length > 0) {
    const key = hits[0].object.userData.sectionKey;
    if (key) window.focusCameraAndOpenModal(key);
  }
}

/* --------------------------------------------------------------------------
   RESIZE + RENDER LOOP
   -------------------------------------------------------------------------- */
function onResize() {
  if (!camera || !renderer) return;
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
  requestAnimationFrame(animate);
  if (controls) controls.update();
  if (renderer && scene && camera) renderer.render(scene, camera);
}

// Monitor scene graph for unexpected visible meshes
setInterval(() => {
  if (scene) {
    scene.traverse(node => {
      if (node.isMesh && node.visible && (node.name.toLowerCase().includes('jesse') || node.name.toLowerCase().includes('zhou'))) {
        console.log('[MONITOR] Unexpected visible mesh found in active scene:', node.name, 'parent:', node.parent ? node.parent.name : 'none');
      }
    });
  }
}, 1000);
