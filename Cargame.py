
from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SUPERCAR | Extreme Racing</title>

<style>
*{box-sizing:border-box}
body{
 margin:0;background:#050812;color:white;
 font-family:Arial,sans-serif;overflow:hidden
}
#game{position:fixed;inset:0}
canvas{display:block}
.hud{
 position:fixed;inset:0;pointer-events:none;
 padding:25px;z-index:2
}
.top{
 display:flex;justify-content:space-between;align-items:flex-start
}
.logo{
 font-size:23px;font-weight:900;letter-spacing:5px;
 text-shadow:0 0 20px #00d9ff
}
.logo small{display:block;font-size:9px;color:#8ea8bd;
 letter-spacing:4px;margin-top:6px}
.stats{display:flex;gap:12px}
.stat{
 background:#071322bb;border:1px solid #ffffff25;
 padding:12px 19px;border-radius:9px;min-width:105px
}
.stat small{display:block;color:#91a9bd;font-size:9px;letter-spacing:2px}
.stat b{display:block;font-size:22px;margin-top:5px}
#speed{color:#54eaff}
#level{color:#ffbf71}
.bottom{
 position:absolute;bottom:25px;left:25px;right:25px;
 display:flex;justify-content:space-between;align-items:end
}
.progressbox{width:min(350px,45vw)}
.progressbox small{color:#9db3c8;font-size:10px;letter-spacing:2px}
.track{height:6px;background:#ffffff20;margin-top:9px;border-radius:10px}
#progress{height:100%;width:0;background:#51eaff;border-radius:10px}
.controls{font-size:11px;color:#a9bfd0;line-height:2;text-align:right}
kbd{
 background:#17283a;border:1px solid #567084;
 padding:5px 8px;border-radius:4px;color:white
}
.overlay{
 position:fixed;inset:0;z-index:5;display:flex;
 align-items:center;justify-content:center;text-align:center;
 background:linear-gradient(120deg,#020711eF,#061a30bb);
 padding:20px
}
.overlay.hide{display:none}
.panel{max-width:650px}
.tag{color:#5beaff;letter-spacing:7px;font-size:11px;font-weight:bold}
h1{font-size:clamp(38px,8vw,83px);line-height:.95;
 margin:20px 0;text-transform:uppercase;letter-spacing:-3px}
h1 span{color:#57e9ff}
.desc{color:#a6bbcd;line-height:1.8;font-size:14px}
button{
 pointer-events:auto;border:0;padding:16px 35px;
 background:linear-gradient(110deg,#50eaff,#b2f8ff);
 color:#03101a;font-weight:900;letter-spacing:2px;
 border-radius:5px;cursor:pointer;margin-top:22px
}
button:hover{filter:brightness(1.2)}
#message{color:#ffc27b;font-size:12px;margin-top:16px}
@media(max-width:600px){
 .hud{padding:12px}.logo{font-size:15px;letter-spacing:2px}
 .stats{gap:5px}.stat{padding:8px;min-width:65px}
 .stat b{font-size:16px}.bottom{left:12px;right:12px;bottom:12px}
 .controls{font-size:9px}
}
</style>
</head>

<body>
<div id="game"></div>

<div class="hud">
 <div class="top">
  <div class="logo">SUPERCAR
   <small>EXTREME RACING EXPERIENCE</small>
  </div>
  <div class="stats">
   <div class="stat"><small>SPEED</small><b id="speed">000</b></div>
   <div class="stat"><small>LEVEL</small><b id="level">01 / 03</b></div>
   <div class="stat"><small>DISTANCE</small><b id="distance">0</b></div>
  </div>
 </div>

 <div class="bottom">
  <div class="progressbox">
   <small id="environment">SNOW MOUNTAIN · LEVEL 01</small>
   <div class="track"><div id="progress"></div></div>
  </div>
  <div class="controls">
   <kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd> DRIVE
   &nbsp; <kbd>SPACE</kbd> NITRO<br>
   <kbd>C</kbd> CAMERA
  </div>
 </div>
</div>

<div class="overlay" id="overlay">
 <div class="panel">
  <div class="tag">THREE WORLDS. THREE SUPERCARS.</div>
  <h1>EXTREME<br><span>RACING</span></h1>
  <p class="desc">
   Conquer frozen mountains, survive muddy roads and dominate
   the neon highway. Unlock a new supercar at every level.
  </p>
  <button id="start">START YOUR ENGINE →</button>
  <div id="message">WASD / ARROW KEYS TO DRIVE</div>
 </div>
</div>

<script type="importmap">
{
 "imports":{
  "three":"https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js",
  "three/addons/":"https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"
 }
}
</script>

<script type="module">
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';

const root = document.getElementById('game');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x91b9d6);
scene.fog = new THREE.Fog(0x91b9d6,35,180);

const camera = new THREE.PerspectiveCamera(
 65,innerWidth/innerHeight,.1,500
);
camera.position.set(0,6,12);

const renderer = new THREE.WebGLRenderer({
 antialias:true, powerPreference:'high-performance'
});
renderer.setSize(innerWidth,innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.15;
root.appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xc5eaff,0x343044,2));

const sun = new THREE.DirectionalLight(0xffffff,3);
sun.position.set(-30,50,25);
sun.castShadow=true;
sun.shadow.mapSize.set(2048,2048);
scene.add(sun);

const fill = new THREE.PointLight(0x35cfff,20,60);
fill.position.set(0,9,-20);
scene.add(fill);

const mat=(color,rough=.6,metal=0)=>new THREE.MeshStandardMaterial({
 color,roughness:rough,metalness:metal
});

const materials={
 snow:mat(0xeaf5ff,.85),
 mud:mat(0x563c29,1),
 highway:mat(0x202531,.8),
 roadLine:mat(0xffffff,.5),
 black:mat(0x080b12,.5),
 glass:mat(0x122f45,.18,.6),
 tire:mat(0x08090c,.9),
 ice:mat(0x8bd9f3,.3),
 tree:mat(0x143e35),
 rock:mat(0x606777),
 building:mat(0x101c31),
 gold:mat(0xffaa39,.25,.7)
};

let car, carWheels=[];
let level=1, distance=0, speed=0;
let playing=false, crashed=false, cameraMode=0;
let steer=0, nitro=false;
let objects=[], roadMarks=[], particles=[];
let spawnTimer=0, worldTimer=0;
const keys={};

const cars=[
 {name:'LAMBORGHINI',color:0xffc21a,power:1.0,model:'/static/models/supercar1.glb'},
 {name:'MCLAREN',color:0xff5429,power:1.3,model:'/static/models/supercar2.glb'},
 {name:'BUGATTI',color:0x137bff,power:1.65,model:'/static/models/supercar3.glb'}
];

function makeCar(color){
 const group=new THREE.Group();
 const bodymat=mat(color,.25,.75);
 const body=new THREE.Mesh(
  new THREE.BoxGeometry(2.15,.58,4.4),bodymat
 );
 body.position.y=.85;
 body.castShadow=true;
 group.add(body);

 // Sculpted hood and roof
 const hood=new THREE.Mesh(
  new THREE.BoxGeometry(1.9,.25,1.55),bodymat
 );
 hood.position.set(0,1.12,-1.15);
 group.add(hood);

 const cabin=new THREE.Mesh(
  new THREE.BoxGeometry(1.55,.72,1.9),materials.glass
 );
 cabin.position.set(0,1.48,.35);
 cabin.castShadow=true;
 group.add(cabin);

 const roof=new THREE.Mesh(
  new THREE.BoxGeometry(1.6,.12,1.45),bodymat
 );
 roof.position.set(0,1.87,.3);
 group.add(roof);

 // Front and rear spoilers
 const spoiler=new THREE.Mesh(
  new THREE.BoxGeometry(2.15,.13,.42),materials.black
 );
 spoiler.position.set(0,1.25,1.95);
 group.add(spoiler);

 // Lights
 for(const x of [-.75,.75]){
  const light=new THREE.Mesh(
   new THREE.BoxGeometry(.35,.12,.1),
   new THREE.MeshBasicMaterial({color:0x9ceeff})
  );
  light.position.set(x,.94,-2.22);
  group.add(light);
 }

 for(const x of [-1,1]){
  for(const z of [-1.35,1.35]){
   const wheel=new THREE.Mesh(
    new THREE.CylinderGeometry(.48,.48,.3,32),
    materials.tire
   );
   wheel.rotation.z=Math.PI/2;
   wheel.position.set(x,.55,z);
   wheel.castShadow=true;
   group.add(wheel);
   carWheels.push(wheel);

   const rim=new THREE.Mesh(
    new THREE.CylinderGeometry(.24,.24,.315,24),
    mat(0xb5c7d8,.2,.9)
   );
   rim.rotation.z=Math.PI/2;
   rim.position.copy(wheel.position);
   group.add(rim);
  }
 }
 group.scale.set(1,1,1);
 return group;
}

const loader=new GLTFLoader();

async function buildCar(){
 if(car)scene.remove(car);
 carWheels=[];
 const data=cars[level-1];
 const fallback=makeCar(data.color);
 car=fallback;
 scene.add(car);

 // Optional Blender GLB model. Fallback car remains if no file exists.
 try{
  const gltf=await loader.loadAsync(data.model);
  if(!playing && !crashed)return;
  const model=gltf.scene;
  const box=new THREE.Box3().setFromObject(model);
  const size=new THREE.Vector3();
  box.getSize(size);
  const scale=4.4/Math.max(size.z,size.x);
  model.scale.setScalar(scale);
  model.position.y=-box.min.y*scale;
  model.rotation.y=Math.PI;
  model.traverse(o=>{
   if(o.isMesh){o.castShadow=true;o.receiveShadow=true;}
  });
  scene.remove(car);
  car=model;
  scene.add(car);
 }catch(e){
  console.log('Using built-in supercar model. Add Blender GLB to:',data.model);
 }
}

function clearWorld(){
 for(const o of objects)scene.remove(o);
 objects=[];
 for(const m of roadMarks)scene.remove(m);
 roadMarks=[];
}

function plane(w,h,material,x,y,z){
 const mesh=new THREE.Mesh(new THREE.PlaneGeometry(w,h),material);
 mesh.rotation.x=-Math.PI/2;
 mesh.position.set(x,y,z);
 mesh.receiveShadow=true;
 scene.add(mesh);
 return mesh;
}

let ground,road,skyLight;

function createWorld(){
 clearWorld();

 const config=[
  {bg:0x91b9d6,fog:0xadcce0,ground:materials.snow,road:materials.ice},
  {bg:0x6a5140,fog:0x76604d,ground:materials.mud,road:materials.mud},
  {bg:0x080e22,fog:0x101a32,ground:mat(0x101827),road:materials.highway}
 ][level-1];

 scene.background.setHex(config.bg);
 scene.fog.color.setHex(config.fog);
 scene.fog.near=35;
 scene.fog.far=level===3?190:140;

 if(ground)scene.remove(ground);
 if(road)scene.remove(road);

 ground=plane(240,500,config.ground,0,-.25,-150);
 road=plane(15,500,config.road,0,0,-150);

 // Road borders
 for(const x of [-7.7,7.7]){
  const edge=plane(.28,500,
   level===3?mat(0x25cfff,.3,.4):mat(0xffffff),
   x,.02,-150);
  objects.push(edge);
 }

 // Road markings
 for(let z=-250;z<40;z+=12){
  const mark=plane(.17,5,
   level===3?mat(0xe5f5ff):mat(0xffffff),
   0,.035,z);
  roadMarks.push(mark);
 }

 // Roadside scenery
 for(let i=0;i<65;i++){
  const side=i%2===0?-1:1;
  const z=-Math.random()*300;
  const x=side*(12+Math.random()*24);
  let obj;

  if(level===1){
   const geo=new THREE.ConeGeometry(2+Math.random()*2,8+Math.random()*10,5);
   obj=new THREE.Mesh(geo,materials.snow);
   obj.position.set(x,geo.parameters.height/2-1,z);
  }else if(level===2){
   const geo=new THREE.ConeGeometry(2,9,7);
   obj=new THREE.Mesh(geo,materials.tree);
   obj.position.set(x,4,z);
  }else{
   const height=8+Math.random()*22;
   obj=new THREE.Mesh(
    new THREE.BoxGeometry(7,height,7),
    materials.building
   );
   obj.position.set(x,height/2-1,z);
   const windowMat=new THREE.MeshBasicMaterial({color:0x27c9ff});
   for(let j=0;j<3;j++){
    const win=new THREE.Mesh(
     new THREE.BoxGeometry(.15,1,1),windowMat
    );
    win.position.set(side===1?-3.55:3.55,j*3-height/2+3,0);
    obj.add(win);
   }
  }
  obj.castShadow=true;
  scene.add(obj);
  objects.push(obj);
 }

 // Nitro light changes with world
 fill.color.setHex(level===3?0x268bff:0x55cfff);
 fill.intensity=level===3?35:12;
}

function spawnObstacle(){
 const x=(Math.random()-.5)*10;
 const group=new THREE.Group();

 if(level===1){
  const rock=new THREE.Mesh(
   new THREE.DodecahedronGeometry(1.2,0),materials.ice
  );
  rock.position.y=1;
  group.add(rock);
 }else if(level===2){
  const rock=new THREE.Mesh(
   new THREE.DodecahedronGeometry(1.3,1),materials.rock
  );
  rock.position.y=1;
  group.add(rock);
 }else{
  const barrier=new THREE.Mesh(
   new THREE.BoxGeometry(2.5,1.4,1.2),
   mat(0xff263e,.4,.3)
  );
  barrier.position.y=.7;
  group.add(barrier);
 }
 group.position.set(x,0,-130);
 scene.add(group);
 objects.push(group);
}

function levelUpdate(){
 const newLevel=distance<500?1:distance<1200?2:3;
 if(newLevel!==level){
  level=newLevel;
  speed=0;
  createWorld();
  buildCar();

  const names=['SNOW MOUNTAIN','MUD OFF-ROAD','HIGHWAY NIGHT RACE'];
  document.getElementById('message').textContent=
   'UNLOCKED: '+cars[level-1].name+' · '+names[level-1];
  document.getElementById('environment').textContent=
   names[level-1]+' · LEVEL 0'+level;
 }
}

function crash(){
 if(crashed)return;
 crashed=true;
 playing=false;
 document.getElementById('message').textContent=
  'DISTANCE: '+Math.floor(distance)+' M · LEVEL '+level;
 document.querySelector('.tag').textContent='RACE COMPLETE';
 document.querySelector('h1').innerHTML='RACE<br><span>OVER</span>';
 document.querySelector('.desc').textContent=
  'Your supercar has stopped. Restart and beat your distance record.';
 document.getElementById('start').textContent='RACE AGAIN →';
 document.getElementById('overlay').classList.remove('hide');
}

function update(dt){
 if(!playing)return;

 const maxSpeed=85*cars[level-1].power;
 const acceleration=nitro?1.5:1;
 speed=Math.min(maxSpeed*acceleration,speed+25*dt);

 const steerInput=(keys.ArrowRight||keys.KeyD?1:0)-
                 (keys.ArrowLeft||keys.KeyA?1:0);

 if(keys.ArrowUp||keys.KeyW)speed=Math.min(maxSpeed*acceleration,speed+30*dt);
 if(keys.ArrowDown||keys.KeyS)speed=Math.max(0,speed-55*dt);

 steer=THREE.MathUtils.lerp(steer,steerInput,.12);
 car.position.x=THREE.MathUtils.clamp(
  car.position.x+steer*13*dt,-5.8,5.8
 );
 car.rotation.z=THREE.MathUtils.lerp(car.rotation.z,-steer*.13,.12);
 car.rotation.y=THREE.MathUtils.lerp(car.rotation.y,-steer*.12,.1);

 for(const w of carWheels)w.rotation.x+=speed*dt*.15;

 const travel=speed*dt*.25;
 distance+=travel;

 // Move road scenery toward the player
 for(const o of objects){
  o.position.z+=travel;
 }
 objects=objects.filter(o=>{
  if(o.position.z>20){scene.remove(o);return false;}
  return true;
 });

 for(const m of roadMarks)m.position.z+=travel;
 for(const m of roadMarks){
  if(m.position.z>15)m.position.z-=300;
 }

 spawnTimer-=dt;
 if(spawnTimer<=0){
  spawnObstacle();
  spawnTimer=Math.max(.8,2.5-speed/100);
 }

 // Collision
 for(const o of objects){
  if(o.children.length && o.position.z>0 && o.position.z<4){
   if(Math.abs(o.position.x-car.position.x)<1.7){
    crash();
    break;
   }
  }
 }

 levelUpdate();

 document.getElementById('speed').textContent=
  String(Math.floor(speed*3)).padStart(3,'0');
 document.getElementById('distance').textContent=
  Math.floor(distance);
 document.getElementById('level').textContent='0'+level+' / 03';

 const progress=level===1?distance/500*100:
                level===2?(distance-500)/700*100:
                (distance-1200)/500*100;
 document.getElementById('progress').style.width=
  Math.max(0,Math.min(100,progress))+'%';
}

function cameraUpdate(dt){
 if(!car)return;
 const target=cameraMode===0?
  new THREE.Vector3(car.position.x,5,car.position.z+11):
  cameraMode===1?
  new THREE.Vector3(car.position.x,2.2,car.position.z+4):
  new THREE.Vector3(car.position.x,12,car.position.z+3);

 camera.position.lerp(target,.06);
 camera.lookAt(car.position.x,1,car.position.z-7);
}

let last=performance.now();
function animate(now){
 requestAnimationFrame(animate);
 const dt=Math.min((now-last)/1000,.04);
 last=now;
 update(dt);
 cameraUpdate(dt);
 renderer.render(scene,camera);
}
requestAnimationFrame(animate);

function startGame(){
 distance=0;speed=0;level=1;crashed=false;
 playing=true;spawnTimer=2;
 if(car)scene.remove(car);
 createWorld();
 buildCar();
 document.getElementById('overlay').classList.add('hide');
 document.querySelector('.tag').textContent=
  'THREE WORLDS. THREE SUPERCARS.';
 document.querySelector('h1').innerHTML=
  'EXTREME<br><span>RACING</span>';
 document.querySelector('.desc').textContent=
  'Conquer frozen mountains, survive muddy roads and dominate the neon highway.';
 document.getElementById('start').textContent='START YOUR ENGINE →';
 document.getElementById('environment').textContent=
  'SNOW MOUNTAIN · LEVEL 01';
}

document.getElementById('start').addEventListener('click',startGame);

window.addEventListener('keydown',e=>{
 keys[e.code]=true;
 if(['Space','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.code))
  e.preventDefault();
 if(e.code==='Space')nitro=true;
 if(e.code==='KeyC'&&!e.repeat)cameraMode=(cameraMode+1)%3;
});
window.addEventListener('keyup',e=>{
 keys[e.code]=false;
 if(e.code==='Space')nitro=false;
});
window.addEventListener('blur',()=>{
 Object.keys(keys).forEach(k=>keys[k]=false);
 nitro=false;
});

window.addEventListener('resize',()=>{
 camera.aspect=innerWidth/innerHeight;
 camera.updateProjectionMatrix();
 renderer.setSize(innerWidth,innerHeight);
});
createWorld();
car=makeCar(cars[0].color);
scene.add(car);
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(PAGE)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
