#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Graph Theory Lab (Logistics & Urban Planning)
อัลกอริทึม: Dijkstra, Prim, Graph Coloring (Welsh-Powell), Network Flow (Edmonds-Karp)

วิธีรัน:
- Windows:  py -3.14 app.py
- macOS/Linux:  python3 app.py
- ติดตั้งครั้งแรก (Windows):  py -3.14 -m pip install -r requirements.txt
- ติดตั้งครั้งแรก (macOS/Linux):  python3 -m pip install -r requirements.txt
- เปิดเบราว์เซอร์อัตโนมัติที่ http://localhost:8765
- มือถือ/แท็บเล็ตใน Wi-Fi เดียวกัน: เปิด URL แบบ LAN ที่แสดงใน Terminal
- จะสร้างไฟล์ graph_lab.html ไว้ข้าง ๆ (การรันอัลกอริทึมต้องเปิดผ่านเซิร์ฟเวอร์นี้)
- ใช้ภาพตกแต่ง city_header.png ซึ่งต้องอยู่โฟลเดอร์เดียวกัน
กด Ctrl+C เพื่อปิด
"""
import http.server
import json
import os
import socket
import sys
import threading
import webbrowser
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

from graph_algorithms import run_algorithm

HTML = r"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="theme-color" content="#1a1c2c">
<link rel="manifest" href="/manifest.webmanifest">
<title>Graph Theory Lab</title>
<link rel="icon" type="image/png" href="web.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@400;700&family=Mitr:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
  --ink:#1a1c2c; --paper:#f4efe1; --navy:#333c57; --yellow:#ffcd75; --green:#a7f070; --dgreen:#38b764;
  --blue:#41a6f6; --dblue:#3b5dc9; --orange:#ef7d57; --red:#b13e53; --purple:#5d275d; --gray:#94b0c2; --cyan:#73eff7;
  --font:'Mitr','Tahoma',sans-serif;
}
*{box-sizing:border-box}
html,body{margin:0;height:100%;overflow:hidden;background:var(--navy);font-family:var(--font);color:var(--ink);
  -webkit-user-select:none;user-select:none;-webkit-tap-highlight-color:transparent;touch-action:manipulation;-webkit-text-size-adjust:100%}
#app{display:flex;flex-direction:column;height:100%;height:100dvh;
  padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left)}
header{position:relative;z-index:10;isolation:isolate;padding-top:46px;background:var(--ink);border-bottom:4px solid #000;flex:0 0 auto}
header::before{content:"";position:absolute;z-index:-1;inset:0;height:46px;background:url('head.png') center center/cover no-repeat;image-rendering:pixelated;pointer-events:none}
.titlebar{position:absolute;inset:0 0 auto;z-index:1;height:46px;display:flex;align-items:center;gap:10px;padding:4px 12px}
.logo{position:relative;display:inline-flex;align-items:center;color:#ffb52e;background:linear-gradient(180deg,#9b5b27 0 20%,#633518 20% 100%);border:3px solid #241b20;border-radius:6px;padding:1px 9px 1px 32px;font-family:'Pixelify Sans','Mitr',sans-serif;font-weight:700;font-size:19px;letter-spacing:1px;text-shadow:2px 2px 0 var(--red),-1px -1px 0 #ffd783;white-space:nowrap;box-shadow:0 0 0 2px #8e5a27,3px 4px 0 #000,inset 0 2px 0 #ffd783}
.logo::before{content:"";position:absolute;inset:-4px;border:1px solid #63c74d;border-radius:8px;pointer-events:none}
.logo-cat{position:absolute;left:-6px;top:-9px;width:30px;height:30px;display:grid;place-items:center;font:20px/1 'Mitr','Tahoma',sans-serif;filter:drop-shadow(2px 2px 0 #000);z-index:2}
.sub{color:#241b20;background:#ffcd75;border:2px solid #281b1b;border-radius:3px;padding:0 6px;font-size:12px;font-weight:500;box-shadow:2px 3px 0 #000;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tabbar{position:relative;z-index:1;display:flex;flex-wrap:nowrap;align-items:center;gap:6px;height:48px;min-width:0;overflow-x:auto;overflow-y:hidden;scrollbar-width:none;padding:4px 9px;background:#604025;border-top:3px solid #b17836;touch-action:pan-x}
.tabbar::-webkit-scrollbar{display:none}
.tabbar .btn{min-height:34px;min-width:0;font-size:12px;padding:3px 8px}
.tabbar .tbtn{flex-direction:row;gap:4px}
.tabbar .tbtn .ic{font-size:15px}
.toolbar-section{flex:0 0 auto;color:#ffcd75;font-size:11px;font-weight:600;white-space:nowrap;padding:0 3px}
.toolbar-divider{flex:0 0 1px;height:24px;background:#d3a45c;margin:0 3px}
.btn{font-family:var(--font);font-size:15px;min-height:44px;min-width:44px;padding:6px 12px;background:#f4dfb5;color:var(--ink);
  border:3px solid #30201b;box-shadow:inset 2px 2px 0 rgba(255,255,255,.72),inset -2px -2px 0 rgba(111,75,43,.26),4px 4px 0 #000;
  cursor:pointer;white-space:nowrap;display:inline-flex;align-items:center;justify-content:center;gap:6px;border-radius:5px;text-decoration:none;
  flex:0 0 auto;transition:transform .08s steps(2,end),box-shadow .08s steps(2,end)}
.btn{font-size:calc(15px * var(--font-scale,1))}
.btn:hover:not(:disabled){transform:translate(-1px,-1px);box-shadow:inset 2px 2px 0 rgba(255,255,255,.72),inset -2px -2px 0 rgba(111,75,43,.26),5px 5px 0 #000}
.btn:active:not(:disabled){transform:translate(4px,4px);box-shadow:inset 2px 2px 0 rgba(255,255,255,.72),inset -2px -2px 0 rgba(111,75,43,.26),0 0 0 #000}
.btn:focus-visible{outline:3px solid var(--blue);outline-offset:2px}
.btn:disabled{opacity:.55;cursor:not-allowed}
.btn.on{background:var(--yellow)}
.btn.primary{background:var(--green)}
.btn.danger{background:var(--orange)}
.btn.mini{min-height:34px;font-size:13px;padding:2px 8px}
.tbtn{flex-direction:column;gap:0;font-size:calc(12px * var(--font-scale,1));min-width:66px;padding:3px 8px;line-height:1.2}
.tbtn .ic{font-size:20px;line-height:1.15}
#hint{background:var(--yellow);border-bottom:3px solid var(--ink);padding:6px 12px;font-size:14px;line-height:1.35;flex:0 0 auto}
#toolStatus{background:#fff9e8;border-bottom:2px solid #6b4727;padding:3px 12px;font-size:12px;line-height:1.3;flex:0 0 auto}
#quickTools{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:6px;margin:8px 0}
#quickTools input{min-width:0;width:100%;font:13px var(--font);padding:6px;border:2px solid var(--ink);background:#fff}
#quickTools .btn{font-size:12px;min-height:36px;padding:3px 6px}
main{flex:1;display:flex;flex-direction:column;min-height:0}
#stage{flex:1;position:relative;min-height:150px;overflow:hidden;background:var(--paper);border:5px solid #6b4727;box-shadow:inset 0 0 0 2px #d3a45c}
#cv{position:absolute;inset:0;touch-action:none;display:block;cursor:crosshair}
#isoRightPane{display:none;position:absolute;left:50%;top:0;right:0;bottom:0;border-left:3px solid #6b4727;background:var(--paper)}
#stage.isomorphism-mode #cv{width:50%}
#stage.isomorphism-mode #isoRightPane{display:block}
#isoCv{position:absolute;inset:0;width:100%;height:100%;display:block;pointer-events:auto;touch-action:none;cursor:crosshair}
.iso-pane-title.left{display:none}
#stage.isomorphism-mode .iso-pane-title.left{display:block}
.iso-pane-title{position:absolute;z-index:2;left:8px;top:8px;background:#fff;border:2px solid var(--ink);box-shadow:2px 2px 0 var(--ink);padding:3px 7px;font-size:12px;font-weight:bold;pointer-events:none}
#isoRightStatus{position:absolute;z-index:2;left:8px;right:8px;top:42px;text-align:center;background:rgba(255,255,255,.9);padding:5px;font-size:12px;pointer-events:none}
#isoMappingLegend{display:none;max-height:125px;overflow:auto;background:#fff;border:2px solid var(--ink);box-shadow:2px 2px 0 var(--ink);padding:6px;gap:6px 10px;flex-wrap:wrap;margin:8px 0}
#isoMappingLegend.visible{display:flex}
.iso-pair-chip{display:inline-flex;align-items:center;gap:4px;font-size:11px;white-space:nowrap}
.iso-pair-chip i{width:11px;height:11px;border:1px solid var(--ink);display:inline-block;flex:0 0 auto}
#stage.isomorphism-mode #zoom{right:calc(50% + 10px)}
#stage.isomorphism-mode #badge{top:42px}
#badge{position:absolute;left:8px;top:8px;background:#fff;border:3px solid var(--ink);box-shadow:3px 3px 0 var(--ink);padding:4px 8px;font-size:13px;pointer-events:none}
#zoom{position:absolute;right:10px;bottom:10px;display:flex;flex-direction:column;gap:8px}
#zoom .btn{font-size:20px;padding:0;width:46px}
#dock{flex:0 0 auto;max-height:48vh;overflow-y:auto;background:#e8e4d8;border-top:4px solid #6b4727;padding:4px 10px 10px;-webkit-overflow-scrolling:touch}
@media (min-width:900px){
  main{flex-direction:row}
  #dock{width:390px;max-height:none;border-top:none;border-left:4px solid #6b4727}
  .scroll{padding:4px 10px 6px}
  .tbtn{min-height:36px;font-size:11px}
  .tbtn .ic{font-size:16px}
  .logo{font-size:15px;letter-spacing:.5px;padding:1px 7px 1px 27px;border-width:2px;box-shadow:0 0 0 2px #8e5a27,2px 3px 0 #000,inset 0 2px 0 #ffd783}
  .logo-cat{left:-5px;top:-7px;width:25px;height:25px;font-size:17px}
  .sub{font-size:10px}
}
.dockhead{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:center;gap:6px;padding-top:6px}
.selected-algorithm{justify-content:flex-start;text-align:left;white-space:normal;min-width:0}
.tab-toggle{font-size:19px;padding:0 10px}
.tabgrid{grid-column:1/-1;display:grid;grid-template-columns:repeat(auto-fill,minmax(100px,1fr));gap:8px;padding:2px 4px 8px 0}
.tabgrid[hidden]{display:none}
.btn.tab{font-size:14px;min-width:0;width:100%;padding:6px 6px;white-space:normal;line-height:1.2;text-align:center}
.learning-tabs,.example-categories{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0 14px}
.learning-tabs .btn,.example-categories .btn{flex:1}

.row{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:8px 0}
.desc{background:#fff9e8;border:3px solid #6b4727;padding:8px 10px;font-size:14px;line-height:1.5;box-shadow:3px 3px 0 #241b20}
.desc .app{display:block;margin-top:4px;color:#257179;font-weight:bold}
label.sel{display:flex;flex-direction:column;font-size:13px;flex:1;min-width:130px;gap:3px}
select{font-family:var(--font);font-size:15px;min-height:44px;border:3px solid var(--ink);background:#fff;padding:4px;border-radius:0;box-shadow:3px 3px 0 var(--ink);color:var(--ink);width:100%}
#mbody input[type=text]{font-family:var(--font);font-size:15px;min-height:44px;border:3px solid var(--ink);background:#fff;padding:6px 8px;border-radius:0;box-shadow:3px 3px 0 var(--ink);color:var(--ink);width:100%;margin-top:4px}
#mbody input[type=number],#mbody textarea{font-family:var(--font);font-size:15px;min-height:44px;border:3px solid var(--ink);background:#fff;padding:6px 8px;border-radius:0;box-shadow:3px 3px 0 var(--ink);color:var(--ink);width:100%;margin-top:4px}
#mbody textarea{min-height:82px;resize:vertical}
.bigbtn{width:100%;font-size:17px;min-height:50px}
.player .btn{flex:1;font-size:18px;padding:4px;min-width:44px}
input[type=range]{flex:1;accent-color:var(--red);height:34px;min-width:120px}
#stepLbl{font-size:13px;min-width:80px;text-align:right}
.speed .btn{flex:1;font-size:14px}
.stepbox{background:var(--ink);color:var(--green);border:3px solid #000;padding:10px 12px;min-height:72px;font-size:15px;line-height:1.55;box-shadow:inset 0 0 0 3px var(--navy);-webkit-user-select:text;user-select:text}
.quiz-choice,.term-button{margin:4px;min-height:40px}
.classic-card{border:2px solid var(--ink);background:#fffbe6;padding:10px;margin:8px 0}
.glossary-list{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:6px}
.knight-board{display:grid;grid-template-columns:repeat(8,minmax(26px,1fr));max-width:440px;border:3px solid var(--ink)}
.knight-square{height:40px;min-width:0;padding:0;border:1px solid var(--ink);font:12px var(--font);box-shadow:none;border-radius:0}
.knight-square.dark{background:#94b0c2}.knight-square.light{background:#fffbe6}
.knight-square.visited{background:var(--green);font-weight:bold}
@keyframes step-arrive{0%{transform:translateY(4px);opacity:.65}55%{transform:translateY(-1px)}100%{transform:translateY(0);opacity:1}}
.stepbox.step-pop{animation:step-arrive .52s ease-out}
@media (prefers-reduced-motion:reduce){.stepbox.step-pop{animation:none}}
.legend{font-size:12px;display:flex;flex-wrap:wrap;gap:6px 12px;margin-top:6px}
.lg{display:inline-flex;align-items:center;gap:5px}
.lg i{display:inline-block;width:16px;height:16px;border:2px solid var(--ink)}
.lg i.ln{height:6px;width:24px;border:none}
.lg i.dash{height:0;width:24px;border:none;border-top:5px dashed var(--red)}
#quick{font-size:13px;background:#fff;border:2px solid var(--ink);padding:4px 8px}
@keyframes blink{50%{background:var(--yellow)}}
.glow{animation:blink .9s steps(2) infinite}
/* modal */
#modal{position:fixed;inset:0;background:rgba(26,28,44,.65);display:flex;align-items:center;justify-content:center;z-index:50;
  padding:calc(env(safe-area-inset-top) + 10px) calc(env(safe-area-inset-right) + 10px) calc(env(safe-area-inset-bottom) + 10px) calc(env(safe-area-inset-left) + 10px)}
#modal.hidden{display:none}
.win{background:#fff;border:4px solid var(--ink);box-shadow:8px 8px 0 #000;max-width:780px;width:100%;max-height:100%;display:flex;flex-direction:column}
.winbar{background:var(--dblue);color:#fff;display:flex;justify-content:space-between;align-items:center;padding:4px 4px 4px 12px;border-bottom:4px solid var(--ink);font-weight:bold;gap:8px}
.winbar .btn{min-height:38px;min-width:38px;padding:0 8px;background:var(--orange)}
#mbody{overflow:auto;padding:14px;-webkit-user-select:text;user-select:text;line-height:1.55;-webkit-overflow-scrolling:touch}
#mbody h3{margin:16px 0 6px;font-size:17px;border-bottom:3px solid var(--ink);display:inline-block}
.hero{background:var(--green);border:3px solid var(--ink);box-shadow:4px 4px 0 var(--ink);padding:12px 14px;font-size:17px;margin-bottom:12px}
.hero.warn{background:var(--yellow)}
.hero.bad{background:var(--orange)}
.bignum{font-size:30px;font-weight:bold;display:inline-block;padding:0 6px;background:#fff;border:3px solid var(--ink);margin-left:4px}
.route{margin-top:8px;line-height:2.1}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin:10px 0}
.card{border:3px solid var(--ink);box-shadow:3px 3px 0 var(--ink);padding:8px 10px;background:#fffbe6}
.card .k{font-size:12px;opacity:.75}
.card .v{font-size:22px;font-weight:bold}
.tw{overflow:auto;max-width:100%}
.tbl{border-collapse:collapse;margin:6px 0;font-size:14px}
.tbl th,.tbl td{border:2px solid var(--ink);padding:4px 9px;text-align:center;white-space:nowrap}
.tbl th{background:var(--yellow)}
.tbl td.l{text-align:left;white-space:normal}
.chip{display:inline-block;border:2px solid var(--ink);padding:1px 8px;margin:2px;background:#fff;box-shadow:2px 2px 0 var(--ink)}
.sw{display:inline-block;width:20px;height:20px;border:3px solid var(--ink);vertical-align:middle;margin-right:6px}
.grp{border:3px solid var(--ink);padding:8px;margin:8px 0;background:#fff;box-shadow:3px 3px 0 var(--ink)}
.grp .gh{display:flex;align-items:center;justify-content:space-between;gap:8px;font-weight:bold;margin-bottom:4px}
.note{background:#fff7d6;border:3px dashed var(--ink);padding:8px 10px;margin-top:12px}
.preview{max-width:100%;border:3px solid var(--ink);display:block;margin-top:10px;-webkit-touch-callout:default;-webkit-user-select:auto;user-select:auto}
.pgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.pcard{border:3px solid var(--ink);box-shadow:4px 4px 0 var(--ink);padding:10px;background:#fffbe6;display:flex;flex-direction:column;gap:8px}
.pcard b{font-size:16px}
.pcard{min-height:190px}
.pcard>span{flex:1}
#hint,#toolStatus,.desc,.note,.classic-card,.tbl{font-size:calc(14px * var(--font-scale,1))}
.stepbox{font-size:calc(15px * var(--font-scale,1))}
.hero{font-size:calc(17px * var(--font-scale,1))}
.quiz-choice.answer-wrong{background:#ffc2c2!important;border-color:#b13e53!important;color:#6e1423!important}
.quiz-choice.answer-correct{background:#b8f3c0!important;border-color:#218344!important;color:#145c2d!important}
#practicePanel{display:none;border:3px solid #6b4727;background:#fff9e8;padding:10px;margin:8px 0;box-shadow:3px 3px 0 var(--ink)}
#practicePanel.open{display:block}
#practicePanel .quiz-choice{white-space:normal}
.vertex-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:8px;margin:10px 0}
.vertex-option{min-width:0;min-height:96px;flex-direction:column;white-space:normal}
.vertex-option img{width:54px;height:54px;object-fit:contain}
.background-preview{width:100%;height:92px;object-fit:cover;border:2px solid var(--ink);background:#fff}
ol.steps li{margin-bottom:6px}
#toast{position:fixed;left:50%;top:calc(env(safe-area-inset-top) + 120px);transform:translateX(-50%);background:var(--ink);color:#fff;
  padding:8px 14px;border:3px solid #fff;box-shadow:4px 4px 0 #000;z-index:60;opacity:0;transition:opacity .2s;pointer-events:none;max-width:90vw;text-align:center;font-size:14px}
</style>
</head>
<body>
<div id="app">
  <header>
    <div class="titlebar"><span class="logo"><span class="logo-cat" aria-hidden="true">🐱</span>GRAPH LAB</span><span class="sub">Logistics &amp; Urban Planning</span></div>
    <nav class="tabbar" id="toolbar" aria-label="ฟังก์ชัน">
      <span class="toolbar-section" id="editToolsLabel">แก้ไขกราฟ</span>
      <button type="button" class="btn tbtn on" data-tool="move" title="ย้าย / เลื่อน"><span class="ic">✋</span>ย้าย / เลื่อน</button>
      <button type="button" class="btn tbtn" data-tool="node" title="เพิ่มจุด"><span class="ic">⬛</span>เพิ่มจุด</button>
      <button type="button" class="btn tbtn" data-tool="edge" title="เชื่อมเส้น"><span class="ic">🔗</span>เชื่อมเส้น</button>
      <button type="button" class="btn tbtn" data-tool="edit" title="แก้ชื่อ / น้ำหนัก"><span class="ic">✏️</span>แก้ชื่อ / น้ำหนัก</button>
      <button type="button" class="btn tbtn" data-tool="style" title="สี / รูปแบบจุดและเส้น"><span class="ic">🎨</span>สี / รูปแบบ</button>
      <button type="button" class="btn tbtn" data-tool="bend" title="ดัดเส้น"><span class="ic">〰️</span>ดัดเส้น</button>
      <button type="button" class="btn tbtn" data-tool="reverse" title="กลับทิศทางเส้น"><span class="ic">↔️</span>กลับทิศเส้น</button>
      <button type="button" class="btn tbtn" data-tool="del" title="ลบ"><span class="ic">🗑️</span>ลบ</button>
      <span class="toolbar-divider" role="separator"></span>
      <span class="toolbar-section" id="otherToolsLabel">กราฟและเครื่องมือ</span>
      <button type="button" class="btn tbtn" id="aDir" title="สลับทิศทาง"><span class="ic" id="dirIc">—</span><span id="dirTxt">ไม่มีทิศ</span></button>
      <button type="button" class="btn tbtn" id="aUndo" title="Undo"><span class="ic">↶</span>Undo</button>
      <button type="button" class="btn tbtn" id="aRedo" title="Redo" disabled><span class="ic">↷</span>Redo</button>
      <button type="button" class="btn tbtn" id="aStraight" title="ทำเส้นตรง"><span class="ic">📏</span>ทำเส้นตรง</button>
      <button type="button" class="btn tbtn" id="aClear" title="ล้างกราฟ"><span class="ic">🧹</span>ล้างกราฟ</button>
      <button type="button" class="btn tbtn" id="aPreset" title="ตัวอย่าง"><span class="ic">📂</span>ตัวอย่าง</button>
      <button type="button" class="btn tbtn" id="aLearning" title="การเรียนรู้"><span class="ic">📚</span>การเรียนรู้</button>
      <button type="button" class="btn tbtn" id="aGenerate" title="สร้างกราฟ"><span class="ic">🧩</span>สร้างกราฟ</button>
      <button type="button" class="btn tbtn" id="aLayout" title="จัดวางกราฟ"><span class="ic">🪄</span>จัดวางกราฟ</button>
      <button type="button" class="btn tbtn" id="aPNG" title="ส่งออก PNG"><span class="ic">🖼️</span>ส่งออก PNG</button>
      <button type="button" class="btn tbtn" id="aExportSteps" title="ส่งออกขั้นตอน"><span class="ic">📄</span>ส่งออกขั้นตอน</button>
      <button type="button" class="btn tbtn" id="aLibrary" title="คลังกราฟ"><span class="ic">🗃️</span>คลังกราฟ</button>
      <button type="button" class="btn tbtn" id="aSettings" title="ตั้งค่าพื้นหลัง / จุดยอด"><span class="ic">⚙️</span></button>
      <button type="button" class="btn tbtn" id="aHelp" title="วิธีใช้" aria-label="วิธีใช้"><span class="ic">❓</span></button>
    </nav>
  </header>
  <div id="hint"></div>
  <div id="toolStatus" role="status" aria-live="polite"></div>
  <main>
    <div id="stage">
      <canvas id="cv"></canvas>
      <div id="badge"></div>
      <div class="iso-pane-title left">กราฟที่ 1</div>
      <div id="isoRightPane" aria-label="กราฟที่สองสำหรับเปรียบเทียบ">
        <canvas id="isoCv"></canvas>
        <div class="iso-pane-title">กราฟที่ 2</div>
        <div id="isoRightStatus">เลือก Isomorphic Graphs แล้วเริ่มเปรียบเทียบเพื่อแสดงกราฟที่สอง</div>
      </div>
      <div id="zoom">
        <button type="button" class="btn" id="zIn" title="ซูมเข้า">+</button>
        <button type="button" class="btn" id="zOut" title="ซูมออก">−</button>
        <button type="button" class="btn" id="zFit" title="จัดกึ่งกลาง">⌖</button>
      </div>
    </div>
    <aside id="dock">
      <aside id="practicePanel" aria-live="polite"></aside>
      <div class="dockhead">
        <button type="button" class="btn tab selected-algorithm" id="currentAlgorithm" aria-label="อัลกอริทึมที่เลือก"></button>
        <button type="button" class="btn tab-toggle" id="toggleTabs" aria-label="เลือกอัลกอริทึมอื่น" aria-expanded="false">▼</button>
        <div class="tabgrid" id="tabs"></div>
      </div>
      <div id="algoDesc" class="desc collapsible"></div>
      <div id="isoMappingLegend" aria-live="polite"></div>
      <div id="quickTools" class="collapsible">
        <input id="nodeSearch" type="search" placeholder="ค้นหาจุดยอด..." aria-label="ค้นหาจุดยอด">
        <button type="button" class="btn" id="searchNode">🔎 ไปยังจุด</button>
        <input id="quickCommand" type="text" placeholder="คำสั่ง: v1-v2:5" aria-label="คำสั่งสร้างเส้น">
        <button type="button" class="btn" id="runCommand">↵ ทำคำสั่ง</button>
      </div>
      <div class="row collapsible" id="selRow">
        <label class="sel" id="lblS"><span id="lblSText">ต้นทาง</span><select id="selS"></select></label>
        <label class="sel" id="lblT"><span id="lblTText">ปลายทาง</span><select id="selT"></select></label>
      </div>
      <div class="row"><button type="button" class="btn primary bigbtn" id="runBtn">▶ เริ่มรัน</button></div>
      <div id="player" class="player">
        <div class="row">
          <button type="button" class="btn" id="bFirst" title="ขั้นแรก">⏮</button>
          <button type="button" class="btn" id="bPrev" title="ย้อน">◀</button>
          <button type="button" class="btn" id="bPlay" title="เล่นอัตโนมัติ">▶</button>
          <button type="button" class="btn" id="bNext" title="ถัดไป">▶|</button>
          <button type="button" class="btn" id="bLast" title="ขั้นสุดท้าย">⏭</button>
        </div>
        <div class="row"><input type="range" id="slider" min="0" max="0" value="0"><span id="stepLbl">ขั้น 0/0</span></div>
        <div class="row speed">
          <button type="button" class="btn" data-sp="0.5">0.5×</button>
          <button type="button" class="btn on" data-sp="1">1×</button>
          <button type="button" class="btn" data-sp="2">2×</button>
          <button type="button" class="btn" data-sp="4">4×</button>
        </div>
        <div id="stepText" class="stepbox"></div>
        <div class="row">
          <button type="button" class="btn" id="sumBtn" style="flex:1">📊 สรุปผล</button>
          <button type="button" class="btn danger" id="clearRunBtn" style="flex:1">✖ ล้างผล</button>
        </div>
      </div>
      <div id="legend" class="legend collapsible"></div>
      <div class="row collapsible"><div id="quick"></div></div>
    </aside>
  </main>
</div>
<div id="modal" class="hidden"><div class="win"><div class="winbar"><span id="mtitle"></span><button type="button" class="btn" id="mclose">✖</button></div><div id="mbody"></div></div></div>
<div id="toast"></div>

<script>
(() => {
'use strict';
const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];
const cv = $('#cv'), ctx = cv.getContext('2d');
const isoCv = $('#isoCv'), isoCtx = isoCv.getContext('2d');
const FONT = "'Mitr',Tahoma,sans-serif";
let INK = '#1a1c2c', PAPER = '#f4efe1';
const PALETTE = ['#ef7d57','#41a6f6','#a7f070','#ffcd75','#f4a6d7','#73eff7','#b13e53','#38b764','#c28a4a','#94b0c2','#5d275d','#3b5dc9','#257179','#d4a5ff','#566c86'];
const NODE_FILL = {current:'#d7263d', consider:'#3a86ff', visited:'#2a9d8f', path:'#f4a261', inS:'#8338ec'};
const EDGE_STY = {
  base:{c:INK,w:3}, consider:{c:'#ef7d57',w:6,hl:1}, soft:{c:'#38b764',w:4}, tree:{c:'#38b764',w:6,hl:1},
  path:{c:'#38b764',w:8,hl:1}, reject:{c:'#94b0c2',w:3,dash:1}, cut:{c:'#b13e53',w:7,dash:1,hl:1},
  flow:{c:'#3b5dc9',w:5,hl:1}, sat:{c:'#5d275d',w:6,hl:1}
};
const EDGE_SURFACES = {
  plain:'เส้นธรรมดา', road:'ถนน', water:'ท่อน้ำ', power:'สายไฟฟ้า',
  gas:'ท่อแก๊ส', rail:'ทางรถไฟ', fiber:'สายสื่อสาร', sewer:'ท่อระบายน้ำ'
};
let NR = 22;
const PARALLEL_CURVE_GAP = 56, MINS = 0.2, MAXS = 4, EPS = 1e-9, LS_KEY = 'graphTheoryLab.v1', UNDO_MAX = 70;
const PREF_KEY = 'graphTheoryLab.preferences.v1', LIB_KEY = 'graphTheoryLab.library.v1';
let preferences = {fontSize:14,nodeSize:22,labelStyle:'v',language:'th',patterns:true,hideLabels:false,hideWeights:false,backgroundColor:'#f4efe1',backgroundImage:'',defaultVertexImage:''};
let library = [];
let vertexOptions = [], backgroundImage = null;
const vertexImageCache = new Map();
const IOS = /iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);

function emptyGraph(){ return {nodes:[], edges:[], directed:false, nextId:1, nextEid:1, source:null, sink:null, colorNames:[]}; }
let G = emptyGraph(), view = {x:0, y:0, s:1}, W = 300, H = 300, DPR = 1;
let isoGraph = null, isoFirstGraph = null, isoView = {x:0, y:0, s:1}, isoMapping = null, isoColors = [], isoEdgePairs = [], isoAnimation = null;
let planarityAnimation = null;
let isoSplitView = false, isoPreviousView = null;
let tool = 'move', selNode = null, isoSelNode = null, undoStack = [], redoStack = [], algo = 'dijkstra';
let activeSide = 'left', lastActiveSide = 'left', sideContext = null;
let run = null, stepIdx = 0, playing = false, timer = null, speed = 1;
let stepFx = null;
let flowAnimationFrame = 0;
const pointers = new Map(); let drag = null, pinch = null, lastTap = {t:0, key:''};
let hoverNode = null, hoverEdge = null, hoverStarted = 0, hoverFrame = 0;
let edgePreview = null, isoEdgePreview = null;

/* ---------- utils ---------- */
const clamp = (v,a,b) => Math.max(a, Math.min(b, v));
const fmt = x => x === Infinity ? '∞' : (Number.isInteger(x) ? String(x) : String(+(+x).toFixed(3)));
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const nodeById = id => G.nodes.find(n => n.id === id);
const nm = id => { const n = nodeById(id); return n ? n.label : '?'; };
const edgeName = e => `${nm(e.u)} ${G.directed ? '→' : '–'} ${nm(e.v)}`;
const cName = i => G.colorNames[i] || `สี ${i+1}`;
const cmpNum = (a,b) => a === b ? 0 : (a < b ? -1 : 1);
const card = (k,v) => `<div class="card"><div class="k">${k}</div><div class="v">${v}</div></div>`;
const appNote = t => `<div class="note">💡 <b>การประยุกต์:</b> ${t}</div>`;
function textOn(hex){ const r=parseInt(hex.slice(1,3),16), g=parseInt(hex.slice(3,5),16), b=parseInt(hex.slice(5,7),16); return (0.299*r+0.587*g+0.114*b) < 140 ? '#ffffff' : INK; }
let toastT;
function toast(msg){ const t=$('#toast'); t.textContent=msg; t.style.opacity=1; clearTimeout(toastT); toastT=setTimeout(()=>t.style.opacity=0, 2000); }
function openModal(title, html){ $('#mtitle').textContent=title; $('#mbody').innerHTML=html; $('#modal').classList.remove('hidden'); $('#mbody').scrollTop=0; }
function closeModal(){ $('#modal').classList.add('hidden'); }
function alertBox(msg){ openModal('⚠ แจ้งเตือน', `<div class="hero warn">${msg}</div>`); }

/* ---------- save / undo ---------- */
function sanitize(g){
  g = Object.assign(emptyGraph(), g);
  g.nodes = (g.nodes||[]).filter(n => n && typeof n.id === 'number');
  g.nodes.forEach(n => {
    if(n.label == null) n.label = 'v'+n.id;
    if(n.color === undefined) n.color = null;
    if(typeof n.vertexImage!=='string'||/[\\/]/.test(n.vertexImage)||!/\.(png|svg)$/i.test(n.vertexImage))delete n.vertexImage;
  });
  const ids = new Set(g.nodes.map(n => n.id));
  g.edges = (g.edges||[]).filter(e => ids.has(e.u) && ids.has(e.v));
  g.edges.forEach(e => {
    e.w = Number(e.w)||0; e.curve = e.curve||0;
    if(e.color === undefined) e.color = null;
    if(!Object.prototype.hasOwnProperty.call(EDGE_SURFACES,e.surface))e.surface='plain';
  });
  g.nextId = Math.max(g.nextId||1, 1, ...g.nodes.map(n => n.id+1));
  g.nextEid = Math.max(g.nextEid||1, 1, ...g.edges.map(e => e.id+1));
  if(!ids.has(g.source)) g.source = null;
  if(!ids.has(g.sink)) g.sink = null;
  if(!Array.isArray(g.colorNames)) g.colorNames = [];
  return g;
}
function save(){
  try{
    const leftGraph=sideContext ? sideContext.graph : G;
    const leftView=sideContext ? sideContext.view : view;
    localStorage.setItem(LS_KEY, JSON.stringify({
      G:leftGraph, view:leftView, tab:algo,
      isoGraph:activeSide==='right' ? G : isoGraph,
      isoView:activeSide==='right' ? view : isoView
    }));
  }catch(error){ console.error('Could not save graph state:',error); }
}
function load(){
  try{
    const d = JSON.parse(localStorage.getItem(LS_KEY));
    if(d && d.G){
      G=sanitize(d.G);
      if(d.view && isFinite(d.view.s)) view=d.view;
      if(d.isoGraph) isoGraph=sanitize(d.isoGraph);
      if(d.isoView && isFinite(d.isoView.s)) isoView=d.isoView;
      return d.tab || 'dijkstra';
    }
  }catch(error){ console.error('Could not load saved graph state:',error); }
  return null;
}
function loadPreferences(){
  try{
    const stored=JSON.parse(localStorage.getItem(PREF_KEY)||'{}');
    preferences={...preferences,...stored};
    library=JSON.parse(localStorage.getItem(LIB_KEY)||'[]');
    if(!Array.isArray(library))throw new Error('ข้อมูลคลังกราฟไม่ใช่รายการ');
  }catch(error){console.error('Could not load preferences or graph library:',error);library=[];}
  if(!/^#[0-9a-f]{6}$/i.test(preferences.backgroundColor))preferences.backgroundColor='#f4efe1';
  if(typeof preferences.backgroundImage!=='string')preferences.backgroundImage='';
  if(typeof preferences.defaultVertexImage!=='string')preferences.defaultVertexImage='';
  preferences.hideLabels=preferences.hideLabels===true;
  preferences.hideWeights=preferences.hideWeights===true;
  loadBackgroundImage();
  applyPreferences();
}
function applyPreferences(){
  INK='#1a1c2c';
  PAPER=preferences.backgroundColor;
  document.documentElement.style.setProperty('--ink',INK);
  document.documentElement.style.setProperty('--paper',PAPER);
  document.documentElement.style.setProperty('--font-scale',String(clamp((Number(preferences.fontSize)||14)/14,0.85,1.6)));
  NR=clamp(Number(preferences.nodeSize)||22,14,40);
  document.documentElement.style.fontSize=`${clamp(Number(preferences.fontSize)||14,12,22)}px`;
  draw();
}
function setUserPreferences(next){
  try{localStorage.setItem(PREF_KEY,JSON.stringify(next));}
  catch(error){console.error('Could not save preferences:',error);toast('บันทึกการตั้งค่าไม่ได้ — พื้นที่จัดเก็บอาจเต็ม');return false;}
  preferences=next;
  loadBackgroundImage();
  applyPreferences();
  return true;
}
function loadBackgroundImage(){
  backgroundImage=null;
  if(!preferences.backgroundImage)return;
  const image=new Image();
  image.onload=()=>{backgroundImage=image;draw();};
  image.onerror=()=>{console.error('Could not load selected graph background image');toast('เปิดภาพพื้นหลังไม่ได้');};
  image.src=preferences.backgroundImage;
}
async function loadVertexOptions(){
  if(vertexOptions.length)return vertexOptions;
  const response=await fetch('/api/vertices');
  const result=await response.json();
  if(!response.ok)throw new Error(result.error||`HTTP ${response.status}`);
  if(!Array.isArray(result.vertices))throw new Error('รายการภาพจุดยอดจากเซิร์ฟเวอร์ไม่ถูกต้อง');
  vertexOptions=result.vertices;
  return vertexOptions;
}
function getVertexImage(filename){
  if(!vertexImageCache.has(filename)){
    const image=new Image();
    image.onload=()=>draw();
    image.onerror=()=>{console.error(`Could not load vertex image ${filename}`);toast(`โหลดภาพจุดยอดไม่ได้: ${filename}`);};
    const option=vertexOptions.find(item=>item.filename===filename);
    image.src=option?.url||(filename.toLowerCase().endsWith('.svg')
      ?`/vertex/vector/${encodeURIComponent(filename)}`
      :`/vertex/thumbs/${encodeURIComponent(filename)}`);
    vertexImageCache.set(filename,image);
  }
  return vertexImageCache.get(filename);
}
function decodeSharedGraph(){
  const match=location.hash.match(/(?:^#|&)graph=([A-Za-z0-9_-]+)/);
  if(!match)return null;
  try{
    const encoded=match[1].replace(/-/g,'+').replace(/_/g,'/');
    const bytes=Uint8Array.from(atob(encoded),character=>character.charCodeAt(0));
    return sanitize(JSON.parse(new TextDecoder().decode(bytes)));
  }catch(error){console.error('Shared graph URL is invalid:',error);return null;}
}
function shareCurrentGraph(){
  const json=JSON.stringify(G),bytes=new TextEncoder().encode(json);
  let binary='';for(const byte of bytes)binary+=String.fromCharCode(byte);
  const url=`${location.origin}${location.pathname}#graph=${btoa(binary).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'')}`;
  if(url.length>8000)return toast('กราฟใหญ่เกินไปสำหรับการแชร์ด้วย URL (จำกัดประมาณ 8 KB)');
  openModal('🔗 แชร์กราฟผ่าน URL',`<p>ข้อมูลกราฟถูกเข้ารหัสไว้ใน URL และไม่ถูกส่งไปบริการภายนอก</p><input id="shareUrl" type="text" readonly value="${esc(url)}"><p><button type="button" class="btn primary" id="copyShareUrl">คัดลอก URL</button></p><p class="note">ผู้รับเปิดลิงก์นี้ในแอปเพื่อโหลดสำเนากราฟที่แชร์</p>`);
  $('#copyShareUrl').onclick=async()=>{
    try{await navigator.clipboard.writeText(url);toast('คัดลอก URL แล้ว');}
    catch(error){console.error('Clipboard access failed:',error);$('#shareUrl').select();toast('เลือก URL แล้ว — คัดลอกด้วย Ctrl+C');}
  };
}
function persistLibrary(){
  try{localStorage.setItem(LIB_KEY,JSON.stringify(library));}
  catch(error){console.error('Could not save graph library:',error);toast('บันทึกคลังกราฟไม่ได้');}
}
function saveCurrentGraph(name){
  const clean=name.trim();
  if(!clean)return toast('กรุณาตั้งชื่อกราฟ');
  library.push({id:`g${Date.now()}${Math.random().toString(36).slice(2,7)}`,name:clean,graph:JSON.parse(JSON.stringify(G)),savedAt:new Date().toISOString()});
  persistLibrary();showGraphLibrary();toast(`บันทึก "${clean}" แล้ว`);
}
function showGraphLibrary(){
  const cards=library.map(item=>`<article class="classic-card"><b>${esc(item.name)}</b><p>|V| ${item.graph.nodes.length} · |E| ${item.graph.edges.length} · ${item.graph.directed?'มีทิศ':'ไม่มีทิศ'}</p>
    <div class="row"><button type="button" class="btn mini primary" data-library-load="${esc(item.id)}">โหลด</button><button type="button" class="btn mini" data-library-compare="${esc(item.id)}">เทียบข้างกัน</button><button type="button" class="btn mini" data-library-share="${esc(item.id)}">แชร์</button><button type="button" class="btn mini danger" data-library-delete="${esc(item.id)}">ลบ</button></div></article>`).join('');
  openModal('🗃️ คลังกราฟในเครื่อง',`<p>คลังกราฟนี้เก็บไว้ใน localStorage ของเบราว์เซอร์เครื่องนี้</p><label class="sel">ชื่อกราฟ<input id="libraryName" type="text" maxlength="80" placeholder="เช่น เครือข่ายรถไฟ"></label><button type="button" class="btn primary" id="saveLibraryGraph">บันทึกกราฟปัจจุบัน</button><button type="button" class="btn" id="shareCurrentGraph">แชร์กราฟปัจจุบัน</button><h3>กราฟที่บันทึก (${library.length})</h3>${cards||'<p>ยังไม่มีกราฟที่บันทึกไว้</p>'}`);
}
async function showSettings(){
  let options=[];
  try{options=await loadVertexOptions();}
  catch(error){console.error('Could not load vertex image list:',error);toast(`โหลดภาพจุดยอดไม่ได้: ${error.message}`);}
  const vertexChoices=options.map(option=>`<option value="${esc(option.filename)}">${esc(option.name)}</option>`).join('');
  openModal('⚙️ พื้นหลังและรูปแบบจุดยอด',`<h3>พื้นหลังพื้นที่กราฟ</h3><label class="sel">สีพื้นหลัง<input id="prefBackgroundColor" type="color" value="${esc(preferences.backgroundColor)}"></label><label class="sel">หรือเลือกภาพจากเครื่อง<input id="prefBackgroundFile" type="file" accept="image/*"></label><button type="button" class="btn mini" id="clearBackgroundImage">ใช้สีเป็นพื้นหลัง</button><img class="background-preview" id="backgroundPreview" alt="ตัวอย่างพื้นหลัง" style="display:none">
    <h3>จุดยอด</h3><label class="sel">ภาพเริ่มต้นสำหรับจุดใหม่<select id="prefDefaultVertex"><option value="">ไม่ใช้ภาพ</option>${vertexChoices}</select></label>
    <label class="sel">ขนาดจุดยอด<select id="prefNode"><option>14</option><option>18</option><option>22</option><option>28</option><option>34</option><option>40</option></select></label>
    <label class="sel">ขนาดตัวอักษร<select id="prefFont"><option>12</option><option>14</option><option>16</option><option>18</option><option>20</option><option>22</option></select></label>
    <label class="sel">รูปแบบชื่อจุดทั่วไป<select id="prefLabels"><option value="v">v1, v2, …</option><option value="letter">A, B, …</option><option value="number">1, 2, …</option></select></label>
    <label class="sel">ภาษาเมนู<select id="prefLanguage"><option value="th">ไทย</option><option value="en">English</option></select></label><label><input id="prefPatterns" type="checkbox"> แสดงลวดลาย/หมายเลขช่วยแยกสี</label>
    <label><input id="prefHideLabels" type="checkbox"> ซ่อนป้ายชื่อจุด</label>
    <label><input id="prefHideWeights" type="checkbox"> ซ่อนน้ำหนักเส้น</label>
    <p class="note">เปลี่ยนภาพของจุดที่มีอยู่: ปิดหน้าต่างนี้ เลือก “สี / รูปแบบ” จากแถบด้านบน แล้วแตะจุด PNG เดิมเป็นภาพ raster จึงไม่สามารถกลายเป็น vector โดยไม่ trace และอาจสูญเสียรายละเอียด; หากมีไฟล์ SVG อยู่แล้ว ให้วางใน vertex แล้วเลือกใช้เป็นภาพ vector ได้โดยตรง</p>`);
  $('#prefFont').value=String(preferences.fontSize);$('#prefNode').value=String(preferences.nodeSize);
  $('#prefLabels').value=preferences.labelStyle;$('#prefLanguage').value=preferences.language;
  $('#prefPatterns').checked=preferences.patterns;$('#prefDefaultVertex').value=preferences.defaultVertexImage;
  $('#prefHideLabels').checked=preferences.hideLabels;$('#prefHideWeights').checked=preferences.hideWeights;
  if(preferences.backgroundImage){const preview=$('#backgroundPreview');preview.src=preferences.backgroundImage;preview.style.display='block';}
  const saveForm=()=>{
    const backgroundColor=$('#prefBackgroundColor').value;
    const colorChanged=backgroundColor!==preferences.backgroundColor;
    const next={...preferences,fontSize:Number($('#prefFont').value),nodeSize:Number($('#prefNode').value),labelStyle:$('#prefLabels').value,language:$('#prefLanguage').value,patterns:$('#prefPatterns').checked,hideLabels:$('#prefHideLabels').checked,hideWeights:$('#prefHideWeights').checked,defaultVertexImage:$('#prefDefaultVertex').value,backgroundColor,backgroundImage:colorChanged?'':preferences.backgroundImage};
    if(setUserPreferences(next)){
      if(colorChanged)$('#backgroundPreview').style.display='none';
      renderMainNavigation();
    }
  };
  $('#mbody').onchange=e=>{
    if(['prefFont','prefNode','prefLabels','prefLanguage','prefPatterns','prefHideLabels','prefHideWeights','prefDefaultVertex','prefBackgroundColor'].includes(e.target.id))saveForm();
    if(e.target.id==='prefBackgroundFile'){
      const file=e.target.files?.[0];if(!file)return;
      if(file.size>4*1024*1024){toast('ภาพพื้นหลังต้องมีขนาดไม่เกิน 4 MB');e.target.value='';return;}
      const reader=new FileReader();
      reader.onerror=()=>{console.error('Could not read background image file');toast('อ่านไฟล์ภาพพื้นหลังไม่ได้');};
      reader.onload=()=>{
        const source=new Image();
        source.onerror=()=>{console.error('Could not decode background image file');toast('ไฟล์นี้ไม่ใช่ภาพที่เปิดได้');};
        source.onload=()=>{
          const scale=Math.min(1,1600/Math.max(source.width,source.height));
          const canvas=document.createElement('canvas');canvas.width=Math.max(1,Math.round(source.width*scale));canvas.height=Math.max(1,Math.round(source.height*scale));
          const context=canvas.getContext('2d');context.fillStyle=preferences.backgroundColor;context.fillRect(0,0,canvas.width,canvas.height);context.drawImage(source,0,0,canvas.width,canvas.height);
          const imageData=canvas.toDataURL('image/webp',0.84);
          const next={...preferences,backgroundImage:imageData};
          if(setUserPreferences(next)){const preview=$('#backgroundPreview');preview.src=preferences.backgroundImage;preview.style.display='block';}
        };
        source.src=String(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };
  $('#clearBackgroundImage').onclick=()=>{
    const next={...preferences,backgroundImage:''};
    if(setUserPreferences(next))$('#backgroundPreview').style.display='none';
  };
}
const TAB_EN={analyze:'Analyze',dijkstra:'Dijkstra',bellmanford:'Bellman–Ford',bfs:'BFS / DFS',prim:'Prim / MST',kruskal:'Kruskal / MST',connectivity:'Connectivity',vertexconnectivity:'Vertex Connectivity',edgeconnectivity:'Edge Connectivity',matching:'Matching',assignment:'Assignment',tspexact:'TSP Exact',tspnearest:'TSP Nearest',tsp2opt:'TSP 2-opt',pruferdecode:'Prufer Decode',havelhakimi:'Degree Sequence',hamiltonian:'Hamiltonian',transform:'Graph Transform',bipartite:'Bipartite',isomorphism:'Isomorphism',euler:'Euler',edgecolor:'Edge Coloring',color:'Vertex Coloring',flow:'Max Flow',planarity:'Planarity'};
function renderMainNavigation(){
  const english=preferences.language==='en';
  $('#editToolsLabel').textContent=english?'Graph editing':'แก้ไขกราฟ';
  $('#otherToolsLabel').textContent=english?'Graph & learning':'กราฟและการเรียนรู้';
  $$('#tabs [data-tab]').forEach(button=>{const tab=TABS[button.dataset.tab];if(tab)button.textContent=`${tab.icon} ${english?(TAB_EN[button.dataset.tab]||tab.name):tab.name}`;});
  const selectedTab=TABS[algo];
  $('#currentAlgorithm').textContent=`${selectedTab.icon} ${english?(TAB_EN[algo]||selectedTab.name):selectedTab.name}`;
  const toolbarLabels=english
    ?{move:'Move / Pan',node:'Add vertex',edge:'Add edge',edit:'Edit label / weight',style:'Color / style',bend:'Bend edge',reverse:'Reverse edge',del:'Delete'}
    :{move:'ย้าย / เลื่อน',node:'เพิ่มจุด',edge:'เชื่อมเส้น',edit:'แก้ชื่อ / น้ำหนัก',style:'สี / รูปแบบ',bend:'ดัดเส้น',reverse:'กลับทิศเส้น',del:'ลบ'};
  Object.entries(toolbarLabels).forEach(([tool,label])=>{
    const button=$(`#toolbar [data-tool="${tool}"]`),icon=button?.querySelector('.ic');
    if(button&&icon)button.replaceChildren(icon,document.createTextNode(label));
  });
  const commandLabels=english
    ?{aStraight:'Straighten edges',aPreset:'Examples',aLearning:'Learning',aGenerate:'Generate graph',aLayout:'Auto layout',aPNG:'Export PNG',aClear:'Clear graph',aExportSteps:'Export steps',aLibrary:'Graph library',aSettings:'Background / vertex settings'}
    :{aStraight:'ทำเส้นตรง',aPreset:'ตัวอย่าง',aLearning:'การเรียนรู้',aGenerate:'สร้างกราฟ',aLayout:'จัดวางกราฟ',aPNG:'ส่งออก PNG',aClear:'ล้างกราฟ',aExportSteps:'ส่งออกขั้นตอน',aLibrary:'คลังกราฟ',aSettings:'ตั้งค่าพื้นหลัง / จุดยอด'};
  Object.entries(commandLabels).forEach(([id,label])=>{
    const button=$(`#${id}`),icon=button?.querySelector('.ic');
    if(button&&icon)button.replaceChildren(icon,document.createTextNode(label));
  });
  $('#aLibrary').textContent=english?'🗃️ Graph library':'🗃️ คลังกราฟ';
  $('#aSettings').textContent='⚙️';
  $('#aSettings').title=english?'Background / vertex settings':'ตั้งค่าพื้นหลัง / จุดยอด';
  $('#aHelp').textContent='❓';
  $('#aHelp').title=english?'Help':'วิธีใช้';
  $('#dirTxt').textContent=english?(G.directed?'Directed':'Undirected'):(G.directed?'มีทิศ':'ไม่มีทิศ');
}
function showStepExport(){
  if(!run)return toast('ยังไม่มีขั้นตอนให้ส่งออก');
  openModal('📄 ส่งออกขั้นตอน',`<p>${esc(TABS[run.key]?.name||run.title)} · ${run.steps.length} ขั้น</p><div class="row"><button type="button" class="btn primary" data-export-steps="csv">ดาวน์โหลด CSV / ตาราง</button><button type="button" class="btn" data-export-steps="text">ดาวน์โหลดข้อความ</button></div><div class="tw"><table class="tbl"><tr><th>ขั้น</th><th>รายละเอียด</th></tr>${run.steps.slice(0,120).map((step,index)=>`<tr><td>${index+1}</td><td class="l">${esc(step.msg)}</td></tr>`).join('')}</table>${run.steps.length>120?'<p>แสดงตัวอย่าง 120 ขั้นแรก; ไฟล์ส่งออกมีครบทุกขั้น</p>':''}</div>`);
}
function downloadSteps(format){
  if(!run)return;
  const rows=[['Step','Description'],...run.steps.map((step,index)=>[String(index+1),step.msg])];
  const content=format==='csv'?rows.map(row=>row.map(value=>`"${String(value).replace(/"/g,'""')}"`).join(',')).join('\r\n'):rows.map(([number,text])=>`${number}. ${text}`).join('\r\n');
  const blob=new Blob([content],{type:format==='csv'?'text/csv;charset=utf-8':'text/plain;charset=utf-8'});
  const url=URL.createObjectURL(blob),link=document.createElement('a');
  link.href=url;link.download=`graph-steps.${format==='csv'?'csv':'txt'}`;link.click();URL.revokeObjectURL(url);
}
function updateHistoryButtons(){
  $('#aUndo').disabled = !undoStack.length;
  $('#aRedo').disabled = !redoStack.length;
}
function pushUndo(){
  undoStack.push({side:activeSide, graph:JSON.stringify(G)});
  if(undoStack.length > UNDO_MAX) undoStack.shift();
  redoStack = [];
  updateHistoryButtons();
}
function graphForSide(side){ return side==='right' ? isoGraph : G; }
function restoreGraphForSide(side, graph){
  if(side==='right') isoGraph=sanitize(graph);
  else G=sanitize(graph);
}
function historyChange(side){
  if(side==='right'){
    if(algo==='isomorphism')invalidateIsomorphismResult();
    isoSelNode=null;isoEdgePreview=null;
    save();updateHistoryButtons();updateBadge();updateHint();
    if(algo==='isomorphism')$('#isoRightStatus').textContent=`กราฟที่สองมี ${isoGraph?isoGraph.nodes.length:0} จุด • ${isoGraph?isoGraph.edges.length:0} เส้น — ใช้เครื่องมือด้านบนแก้ไขได้`;
    draw();
  }else{
    selNode=null;edgePreview=null;afterChange();
  }
}
function undo(){
  if(!undoStack.length) return toast('ไม่มีขั้นให้ย้อนแล้ว');
  const entry=undoStack.pop(), current=graphForSide(entry.side) || emptyGraph();
  redoStack.push({side:entry.side,graph:JSON.stringify(current)});
  if(redoStack.length > UNDO_MAX) redoStack.shift();
  restoreGraphForSide(entry.side,JSON.parse(entry.graph)); clearRun(); historyChange(entry.side);
  toast(`↶ ย้อนแล้ว (ไปข้างหน้าได้อีก ${redoStack.length} ขั้น)`);
}
function redo(){
  if(!redoStack.length) return toast('ไม่มีขั้นให้ไปข้างหน้าแล้ว');
  const entry=redoStack.pop(), current=graphForSide(entry.side) || emptyGraph();
  undoStack.push({side:entry.side,graph:JSON.stringify(current)});
  if(undoStack.length > UNDO_MAX) undoStack.shift();
  restoreGraphForSide(entry.side,JSON.parse(entry.graph)); clearRun(); historyChange(entry.side);
  toast(`↷ ไปข้างหน้าแล้ว (ไปข้างหน้าได้อีก ${redoStack.length} ขั้น)`);
}
function commit(fn, invalidate = true){ pushUndo(); fn(); if(invalidate) clearRun(); afterChange(); }
function afterChange(){
  if(algo==='isomorphism') invalidateIsomorphismResult();
  save(); updateHistoryButtons(); draw();
  if(activeSide==='right') return;
  refreshSelects(); updateBadge(); updateHint();
}

function withCanvasSide(side, action){
  if(side!=='right' || !isoSplitView){ activeSide='left';lastActiveSide='left';return action(); }
  const previous={G,view,selNode,edgePreview};
  sideContext={graph:G,view};
  G=isoGraph || emptyGraph();
  if(!isoGraph) G.directed=previous.G.directed;
  view=isoView;
  selNode=isoSelNode;
  edgePreview=isoEdgePreview;
  activeSide='right';lastActiveSide='right';
  try{ return action(); }
  finally{
    isoGraph=G;isoView=view;isoSelNode=selNode;isoEdgePreview=edgePreview;
    G=previous.G;view=previous.view;selNode=previous.selNode;edgePreview=previous.edgePreview;
    activeSide='left';sideContext=null;
    updateHistoryButtons();updateBadge();updateHint();
      if(algo==='isomorphism'&&!isoFirstGraph&&isoGraph){
      $('#isoRightStatus').textContent=`กราฟที่สองมี ${isoGraph.nodes.length} จุด • ${isoGraph.edges.length} เส้น — ใช้เครื่องมือด้านบนแก้ไขได้`;
    }
    draw();
  }
}
function withLastCanvasSide(action){
  return withCanvasSide(lastActiveSide,action);
}

/* ---------- geometry ---------- */
function toWorld(sx, sy){ return {x:(sx-view.x)/view.s, y:(sy-view.y)/view.s}; }
function parallelEdgeCurves(graph){
  const groups=new Map(),curves=new Map();
  for(const edge of graph.edges){
    const key=edge.u===edge.v?`loop:${edge.u}`:`pair:${Math.min(edge.u,edge.v)}:${Math.max(edge.u,edge.v)}`;
    if(!groups.has(key))groups.set(key,[]);
    groups.get(key).push(edge);
  }
  for(const group of groups.values()){
    if(group.length<2)continue;
    group.sort((a,b)=>a.id-b.id);
    group.forEach((edge,index)=>curves.set(edge.id,(index-(group.length-1)/2)*PARALLEL_CURVE_GAP));
  }
  return curves;
}
function edgeGeom(e, curveMap=null){
  const a = nodeById(e.u), b = nodeById(e.v); if(!a || !b) return null;
  const curve=curveMap&&curveMap.has(e.id)?curveMap.get(e.id)*(e.u<=e.v?1:-1):(e.curve||0);
  if(a === b){
    const offset = curve, lift = 48 + Math.abs(offset);
    return {a:{x:a.x-12,y:a.y-17},b:{x:a.x+12,y:a.y-17},mx:a.x+offset,my:a.y-lift/2,
      nx:1,ny:0,cx:a.x+offset,cy:a.y-lift,px:a.x+offset,py:a.y-lift/2};
  }
  const mx=(a.x+b.x)/2, my=(a.y+b.y)/2, dx=b.x-a.x, dy=b.y-a.y, L=Math.hypot(dx,dy)||1;
  const nx=-dy/L, ny=dx/L, c=curve;
  return {a, b, mx, my, nx, ny, cx:mx+nx*c*2, cy:my+ny*c*2, px:mx+nx*c, py:my+ny*c};
}
function bez(g, t){ const u=1-t; return {x:u*u*g.a.x+2*u*t*g.cx+t*t*g.b.x, y:u*u*g.a.y+2*u*t*g.cy+t*t*g.b.y}; }
function distSeg(p, a, b){ const dx=b.x-a.x, dy=b.y-a.y, L=dx*dx+dy*dy; let t=L?((p.x-a.x)*dx+(p.y-a.y)*dy)/L:0; t=clamp(t,0,1); return Math.hypot(p.x-(a.x+t*dx), p.y-(a.y+t*dy)); }
function hitNode(w){ const r=NR+6/view.s; for(let i=G.nodes.length-1;i>=0;i--){ const n=G.nodes[i]; if(Math.abs(w.x-n.x)<=r && Math.abs(w.y-n.y)<=r) return n; } return null; }
function hitEdge(w){
  const tol = 12/view.s, curveMap=parallelEdgeCurves(G); let best=null, bd=tol;
  for(const e of G.edges){
    const g = edgeGeom(e,curveMap); if(!g) continue;
    const dl = Math.hypot(w.x-g.px, w.y-g.py); if(dl < 16/view.s && dl < bd){ bd=dl; best=e; }
    let prev = bez(g,0);
    for(let i=1;i<=24;i++){ const p=bez(g,i/24); const d=distSeg(w,prev,p); if(d<bd){ bd=d; best=e; } prev=p; }
  }
  return best;
}

/* ---------- rendering ---------- */
function resize(){
  const r = $('#stage').getBoundingClientRect(); DPR = window.devicePixelRatio || 1;
  W = Math.max(1, isoSplitView ? r.width/2 : r.width); H = Math.max(1, r.height);
  cv.width = Math.round(W*DPR); cv.height = Math.round(H*DPR); cv.style.width = W+'px'; cv.style.height = H+'px';
  if(isoSplitView){
    const rightW = Math.max(1, r.width-W);
    isoCv.width = Math.round(rightW*DPR); isoCv.height = Math.round(H*DPR);
    isoCv.style.width = rightW+'px'; isoCv.style.height = H+'px';
  }
  draw();
}
function currentStep(){ return run ? run.steps[stepIdx] : null; }
function draw(){
  ctx.setTransform(DPR,0,0,DPR,0,0);
  renderScene(ctx, W, H, view, algo === 'isomorphism' && isoFirstGraph ? isoFirstGraph : G, algo === 'isomorphism' ? null : undefined, false);
  if(isoSplitView){
    const r = $('#stage').getBoundingClientRect(), rightW = Math.max(1,r.width-W);
    isoCtx.setTransform(DPR,0,0,DPR,0,0);
    if(isoGraph) renderScene(isoCtx, rightW, H, isoView, isoGraph, null, true);
    else { isoCtx.clearRect(0,0,rightW,H); isoCtx.fillStyle=PAPER; isoCtx.fillRect(0,0,rightW,H); }
  }
  const flowStep = currentStep();
  const hasVisibleFlow = flowStep && flowStep.etext &&
    Object.values(flowStep.etext).some(text => Number.parseFloat(text) > EPS);
  const animateFlow = algo === 'flow' && G.directed && hasVisibleFlow &&
    !(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  if(animateFlow && !flowAnimationFrame){
    flowAnimationFrame = requestAnimationFrame(() => {
      flowAnimationFrame = 0;
      if(algo === 'flow' && G.directed) draw();
    });
  }else if(!animateFlow && flowAnimationFrame){
    cancelAnimationFrame(flowAnimationFrame);
    flowAnimationFrame = 0;
  }
}
const CURSOR_STYLES = {
  move: 'grab',
  node: 'crosshair',
  edge: 'crosshair',
  edit: 'text',
  bend: 'move',
  reverse: 'crosshair',
  del: 'not-allowed',
  style: 'pointer'
};
function updateCanvasCursor(){
  cv.style.cursor = CURSOR_STYLES[tool] || 'default';
  isoCv.style.cursor = CURSOR_STYLES[tool] || 'default';
}
function setHover(node, edge){
  const nodeId = node ? node.id : null, edgeId = edge ? edge.id : null;
  updateCanvasCursor();
  if(nodeId === hoverNode && edgeId === hoverEdge) return;
  hoverNode = nodeId; hoverEdge = edgeId; hoverStarted = performance.now();
  updateCanvasCursor();
  draw();
  if((node || edge) && !hoverFrame) hoverFrame = requestAnimationFrame(animateHover);
}
function animateHover(){
  if(hoverNode == null && hoverEdge == null){ hoverFrame = 0; return; }
  draw(); hoverFrame = requestAnimationFrame(animateHover);
}
function renderScene(c, w, h, v, graph=G, stepOverride=undefined, comparisonPanel=false){
  const previousGraph=G; G=graph;
  try{
    c.fillStyle = PAPER; c.fillRect(0,0,w,h);
    if(backgroundImage){
      const scale=Math.max(w/backgroundImage.width,h/backgroundImage.height);
      const imageWidth=backgroundImage.width*scale,imageHeight=backgroundImage.height*scale;
      c.drawImage(backgroundImage,(w-imageWidth)/2,(h-imageHeight)/2,imageWidth,imageHeight);
    }
    const gs = 40*v.s;
    if(gs > 12){
      c.fillStyle = '#d6cdb5';
      const ox = ((v.x%gs)+gs)%gs, oy = ((v.y%gs)+gs)%gs;
      for(let x=ox;x<w;x+=gs) for(let y=oy;y<h;y+=gs) c.fillRect(Math.round(x)-1, Math.round(y)-1, 3, 3);
    }
    c.save(); c.translate(v.x, v.y); c.scale(v.s, v.s);
    const st = stepOverride === undefined ? currentStep() : stepOverride, showW = algo !== 'color' && !preferences.hideWeights;
    const curveMap=parallelEdgeCurves(G);
    for(const e of G.edges) drawEdge(c, e, st, showW, comparisonPanel, curveMap);
    const preview=graph===isoGraph ? {node:isoSelNode,point:isoEdgePreview} : {node:selNode,point:edgePreview};
    if(tool==='edge' && preview.node!=null && preview.point) drawEdgePreview(c,preview.node,preview.point);
    for(const n of G.nodes) drawNode(c, n, st, comparisonPanel);
    c.restore();
  }finally{ G=previousGraph; }
}
function drawEdgePreview(c, sourceId, target){
  const source = nodeById(sourceId); if(!source) return;
  const dx = target.x-source.x, dy = target.y-source.y, length = Math.hypot(dx,dy);
  if(length < 1) return;
  const ux = dx/length, uy = dy/length, endNode = hitNode(target);
  const start = {x:source.x+ux*NR, y:source.y+uy*NR};
  const endDistance = endNode && endNode.id !== sourceId ? Math.max(NR, length-NR) : length;
  const end = {x:source.x+ux*endDistance, y:source.y+uy*endDistance};
  c.save(); c.beginPath(); c.moveTo(start.x,start.y); c.lineTo(end.x,end.y);
  c.setLineDash([8,6]); c.lineWidth=4; c.strokeStyle='#ffcd75'; c.lineCap='round';
  c.shadowColor=INK; c.shadowBlur=2; c.stroke(); c.restore();
}
function pill(c, x, y, text, bg, fg, border){
  c.font = `bold 13px ${FONT}`;
  const tw = c.measureText(text).width, pw = tw+12, ph = 20;
  c.fillStyle = INK; c.fillRect(x-pw/2+2, y-ph/2+2, pw, ph);
  c.fillStyle = bg; c.fillRect(x-pw/2, y-ph/2, pw, ph);
  c.lineWidth = 2; c.strokeStyle = border || INK; c.strokeRect(x-pw/2, y-ph/2, pw, ph);
  c.fillStyle = fg; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(text, x, y+1);
}
function tag(c, x, y, t, bg){
  c.fillStyle = INK; c.fillRect(x-9, y-9, 18, 18);
  c.fillStyle = bg; c.fillRect(x-7, y-7, 14, 14);
  c.fillStyle = '#fff'; c.font = `bold 11px ${FONT}`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(t, x, y+1);
}
function roundedBox(c, x, y, size, radius=6){
  const r = Math.min(radius, size/2);
  c.beginPath(); c.moveTo(x+r,y); c.lineTo(x+size-r,y); c.quadraticCurveTo(x+size,y,x+size,y+r);
  c.lineTo(x+size,y+size-r); c.quadraticCurveTo(x+size,y+size,x+size-r,y+size);
  c.lineTo(x+r,y+size); c.quadraticCurveTo(x,y+size,x,y+size-r);
  c.lineTo(x,y+r); c.quadraticCurveTo(x,y,x+r,y); c.closePath();
}
function drawEdge(c, e, st, showW, comparisonPanel=false, curveMap=null){
  const g = edgeGeom(e,curveMap); if(!g) return;
  const isoPairIndex=algo==='isomorphism'&&isoMapping
    ?isoEdgePairs.findIndex(pair=>(comparisonPanel?pair.rightId:pair.leftId)===e.id):-1;
  const edgeStep=stepIdx-isoColors.length;
  const isoMatched=isoPairIndex>=0&&edgeStep>isoPairIndex;
  const hovered = !comparisonPanel && hoverEdge === e.id;
  const key = isoMatched?'path':comparisonPanel&&algo==='isomorphism'&&isoMapping?'reject':st&&st.edge?st.edge[e.id]:null;
  const S = EDGE_STY[key] || EDGE_STY.base;
  const phase=key?stepFxPhase():0,pulse=key?Math.sin(Math.PI*phase):0;
  const flowValue = st && st.etext ? Number.parseFloat(st.etext[e.id]) : 0;
  const isFlowPipe = !comparisonPanel && algo === 'flow' && G.directed && flowValue > EPS;
  const surfaceProgress = surfaceBuildProgress(e, comparisonPanel);
  const isBuildingSurface = surfaceProgress>0&&surfaceProgress<1;
  if(hovered){
    const wobble = Math.sin((performance.now()-hoverStarted)/75)*2.5;
    g.cx += g.nx*wobble; g.cy += g.ny*wobble; g.px += g.nx*wobble/2; g.py += g.ny*wobble/2;
  }
  const path = () => { c.beginPath(); c.moveTo(g.a.x,g.a.y); c.quadraticCurveTo(g.cx,g.cy,g.b.x,g.b.y); };
  c.save(); c.lineCap = 'round'; c.lineJoin = 'round';
  if(pulse>0){
    c.save(); c.globalAlpha=0.16+0.28*pulse; c.strokeStyle=S.c; c.lineWidth=S.w+10*pulse; c.shadowColor=S.c; c.shadowBlur=14*pulse; path(); c.stroke(); c.restore();
  }
  const isoColor=isoMatched?isoEdgePairs[isoPairIndex].color:null;
  const edgeColor = isFlowPipe
    ? (key === 'cut' ? S.c : key === 'sat' ? '#7851b8' : '#3688c8')
    : (isoColor||(!key && e.color != null ? PALETTE[e.color % PALETTE.length] : S.c));
  if(key){
    c.save();c.globalAlpha=key==='soft'?0.24:0.32;c.strokeStyle=S.c;c.lineWidth=S.w+12;
    c.shadowColor=S.c;c.shadowBlur=12;path();c.stroke();c.restore();
  }
  if(isFlowPipe){
    c.setLineDash([]);
    path(); c.strokeStyle='#253247'; c.lineWidth=15; c.stroke();
    path(); c.strokeStyle=hovered?'#d9e4ed':'#a9bac8'; c.lineWidth=11; c.stroke();
    path(); c.strokeStyle=key==='sat'?'#7954b5':'#247fc7'; c.lineWidth=6; c.stroke();
    if(key && key!=='flow' && key!=='sat'){
      c.setLineDash(S.dash?[10,8]:[]);
      path(); c.strokeStyle=S.c; c.lineWidth=2.5; c.stroke();
    }
    c.setLineDash([2,10]);
    c.lineDashOffset=-(performance.now()/55%12);
    path(); c.strokeStyle='#c8f7ff'; c.lineWidth=2.5; c.stroke();
    c.setLineDash([]); c.lineDashOffset=0;
  }else if(e.surface&&e.surface!=='plain'&&surfaceProgress>0){
    drawStyledEdge(c,e,path,g,edgeColor,key,hovered,surfaceProgress);
  }else{
    if(S.hl){ c.setLineDash([]); c.strokeStyle = INK; c.lineWidth = S.w+4; path(); c.stroke(); }
    c.setLineDash(preferences.patterns&&e.color!=null?[4+(e.color%3)*3,4]:S.dash?[12,8]:[]); c.strokeStyle = hovered ? '#ef7d57' : edgeColor; c.lineWidth = S.w+(hovered?3:0); path(); c.stroke(); c.setLineDash([]);
  }
  if(G.directed&&!isBuildingSurface){
    let t1 = 1;
    for(let i=0;i<=60;i++){ const t=1-i/60, p=bez(g,t); if(Math.abs(p.x-g.b.x)>NR+4 || Math.abs(p.y-g.b.y)>NR+4){ t1=t; break; } }
    const tip = bez(g,t1);
    const dx = 2*(1-t1)*(g.cx-g.a.x)+2*t1*(g.b.x-g.cx), dy = 2*(1-t1)*(g.cy-g.a.y)+2*t1*(g.b.y-g.cy);
    const L = Math.hypot(dx,dy)||1, ux = dx/L, uy = dy/L, sz = 10+S.w;
    c.beginPath(); c.moveTo(tip.x, tip.y);
    c.lineTo(tip.x-ux*sz-uy*sz*0.55, tip.y-uy*sz+ux*sz*0.55);
    c.lineTo(tip.x-ux*sz+uy*sz*0.55, tip.y-uy*sz-ux*sz*0.55); c.closePath();
    c.fillStyle = edgeColor; c.fill(); c.lineWidth = 2; c.strokeStyle = INK; c.stroke();
  }
  const txt = preferences.hideWeights ? null : (st && st.etext ? st.etext[e.id] : (showW ? fmt(e.w) : null));
  if(txt != null) pill(c, g.px, g.py, txt, '#ffffff', INK, S.hl ? S.c : INK);
  if(key==='consider'&&phase>0){
    const spark=bez(g,0.12+0.76*phase);
    c.save();c.fillStyle='#ffcd75';c.shadowColor='#ffcd75';c.shadowBlur=8;
    c.fillRect(spark.x-4,spark.y-4,8,8);c.fillStyle='#ffffff';c.fillRect(spark.x-1,spark.y-1,2,2);c.restore();
  }
  c.restore();
}
function surfaceBuildProgress(edge,comparisonPanel){
  if(comparisonPanel||edge.surface==='plain')return 0;
  if(!run) return 1;
  const current = currentStep();
  if(!current || !current.edge || !Object.prototype.hasOwnProperty.call(current.edge, edge.id)) return 0;
  let firstStep=-1;
  for(let index=0;index<=stepIdx;index++){
    const stepEdge = run.steps[index]?.edge;
    if(stepEdge && Object.prototype.hasOwnProperty.call(stepEdge, edge.id)){firstStep=index;break;}
  }
  if(firstStep<0)return 0;
  if(firstStep<stepIdx||!stepFx)return 1;
  return stepFxPhase();
}
function drawStyledEdge(c,e,path,g,edgeColor,key,hovered,progress=1){
  c.setLineDash([]);c.lineDashOffset=0;
  const surfacePath=()=>{
    if(progress>=1){path();return;}
    const t=clamp(progress,0,1),inverse=1-t;
    const controlX=g.a.x+(g.cx-g.a.x)*t,controlY=g.a.y+(g.cy-g.a.y)*t;
    const endX=inverse*inverse*g.a.x+2*inverse*t*g.cx+t*t*g.b.x;
    const endY=inverse*inverse*g.a.y+2*inverse*t*g.cy+t*t*g.b.y;
    c.beginPath();c.moveTo(g.a.x,g.a.y);c.quadraticCurveTo(controlX,controlY,endX,endY);
  };
  const stroke=(color,width,dash=[])=>{surfacePath();c.strokeStyle=color;c.lineWidth=width;c.setLineDash(dash);c.stroke();};
  if(e.surface==='road'){
    stroke('#202536',16);stroke(hovered?'#6a7180':'#4c5563',12);
    stroke('#ffe17a',2,[10,12]);
  }else if(e.surface==='water'){
    stroke('#263648',16);stroke('#b6c8d4',12);stroke('#2788d0',6);
    c.lineDashOffset=-(performance.now()/55%12);stroke('#d7f8ff',2,[2,10]);
  }else if(e.surface==='power'){
    stroke('#30201b',12);stroke(edgeColor==='#38b764'?'#ffcd75':edgeColor,5);
    c.save();c.translate(g.px,g.py);c.fillStyle='#ffcd75';c.strokeStyle=INK;c.lineWidth=1.5;
    c.beginPath();c.moveTo(1,-9);c.lineTo(-6,1);c.lineTo(-1,1);c.lineTo(-3,9);c.lineTo(7,-3);c.lineTo(1,-3);c.closePath();c.fill();c.stroke();c.restore();
  }else if(e.surface==='gas'){
    stroke('#503e2a',15);stroke('#d9a441',10);stroke('#fff0a8',2,[3,8]);
  }else if(e.surface==='rail'){
    stroke('#454753',13);
    const length=Math.hypot(g.b.x-g.a.x,g.b.y-g.a.y)||1,nx=-(g.b.y-g.a.y)/length,ny=(g.b.x-g.a.x)/length;
    const rail=(offset,color,width,dash=[])=>{
      c.beginPath();c.moveTo(g.a.x+nx*offset,g.a.y+ny*offset);
      c.quadraticCurveTo(g.cx+nx*offset,g.cy+ny*offset,g.b.x+nx*offset,g.b.y+ny*offset);
      c.strokeStyle=color;c.lineWidth=width;c.setLineDash(dash);c.stroke();
    };
    rail(4,'#c4ccd4',3);rail(-4,'#c4ccd4',3);rail(0,'#27303d',8,[2,9]);
  }else if(e.surface==='fiber'){
    stroke('#342253',13);stroke('#9f75e8',8);stroke('#76f1ff',3,[2,7]);
  }else if(e.surface==='sewer'){
    stroke('#3f454c',16);stroke('#818a8c',11);stroke('#36404a',4,[3,8]);
  }
  if(e.color!=null&&preferences.patterns){c.globalAlpha=.85;stroke(PALETTE[e.color%PALETTE.length],2,[1,14]);c.globalAlpha=1;}
  if(key){c.globalAlpha=.92;stroke(EDGE_STY[key]?.c||'#ef7d57',2.5,[8,6]);c.globalAlpha=1;}
  c.setLineDash([]);c.lineDashOffset=0;
}
function drawNode(c, n, st, comparisonPanel=false){
  const hovered = !comparisonPanel && hoverNode === n.id;
  const sty = st && st.node ? st.node[n.id] : null, r = NR;
  const pulse=!comparisonPanel&&(sty==='current'||sty==='consider')?stepFxProgress():0;
  if(hovered||pulse>0){
    c.save();
  }
  if(hovered){
    const phase = (performance.now()-hoverStarted)/75;
    c.translate(n.x,n.y); c.rotate(Math.sin(phase)*0.035);
    const scale = 1.04+Math.sin(phase*2)*0.025; c.scale(scale,scale); c.translate(-n.x,-n.y);
  }
  if(pulse>0){c.translate(n.x,n.y-3*pulse);c.scale(1+0.07*pulse,1+0.07*pulse);c.translate(-n.x,-n.y);}
  let fill = '#8bea3c';
  if(st && st.fill){ if(st.fill[n.id] != null) fill = PALETTE[st.fill[n.id] % PALETTE.length]; }
  else if(!st && n.color != null) fill = PALETTE[n.color % PALETTE.length];
  if(!(st && st.fill) && sty && NODE_FILL[sty]) fill = NODE_FILL[sty];
  let ring = null; if(sty === 'current') ring = '#b13e53'; if((comparisonPanel?isoSelNode:selNode)===n.id) ring = '#41a6f6';
  const vertexColorIndex=st&&st.fill
    ?(st.fill[n.id] == null ? null : st.fill[n.id])
    :n.color;
  const sourceVertexImage=n.vertexImage?getVertexImage(n.vertexImage):null;
  const vertexImage=sourceVertexImage;
  if(vertexImage&&vertexImage.complete&&vertexImage.naturalWidth){
    const size=2*r+12;
    c.save();
    if(ring){c.shadowColor=ring;c.shadowBlur=12;}
    c.drawImage(vertexImage,n.x-size/2,n.y-size/2,size,size);
    c.restore();
  }else{
    if(ring){ roundedBox(c, n.x-r-8, n.y-r-8, 2*r+16, 10); c.fillStyle = ring; c.fill(); c.strokeStyle = INK; c.lineWidth = 2; c.stroke(); }
    roundedBox(c, n.x-r+5, n.y-r+5, 2*r, 9); c.fillStyle = 'rgba(26,28,44,0.9)'; c.fill();
    roundedBox(c, n.x-r, n.y-r, 2*r, 9); c.fillStyle = fill; c.fill(); c.lineWidth = 3; c.strokeStyle = INK; c.stroke();
    c.fillStyle = 'rgba(255,255,255,0.85)'; c.fillRect(n.x-r+5, n.y-r+5, 7, 4); c.fillRect(n.x-r+5, n.y-r+9, 4, 5);
    c.fillStyle = 'rgba(26,28,44,0.18)'; c.fillRect(n.x+r-6, n.y-r+8, 3, 2*r-16); c.fillRect(n.x-r+8, n.y+r-6, 2*r-16, 3);
  }
  const label=preferences.labelStyle==='letter'&&/^v\d+$/.test(n.label)
    ? String.fromCharCode(65+(n.id-1)%26)+(n.id>26?Math.floor((n.id-1)/26):'')
    : preferences.labelStyle==='number'&&/^v\d+$/.test(n.label)?String(n.id):n.label;
  const short = label.length <= 4, numericLabel = /^\d+$/.test(label);
  if(!preferences.hideLabels&&!vertexImage){
    c.fillStyle = textOn(fill); c.font = `bold ${numericLabel?16:(short?14:12)}px ${numericLabel?"Arial,Tahoma,sans-serif":FONT}`; c.textAlign = 'center'; c.textBaseline = 'middle';
    c.fillText(label, n.x, n.y+1);
  }
  if(preferences.patterns){
    const marker=String((n.id-1)%9+1);
    c.beginPath();c.arc(n.x+r-1,n.y-r+1,7,0,Math.PI*2);c.fillStyle=INK;c.fill();
    c.fillStyle='#fff';c.font='bold 9px Arial,sans-serif';c.textAlign='center';c.textBaseline='middle';c.fillText(marker,n.x+r-1,n.y-r+1);
  }
  if(!preferences.hideLabels&&(!short||vertexImage)){
    const labelBackground=vertexImage&&vertexColorIndex!=null?PALETTE[vertexColorIndex%PALETTE.length]:'#fffbe6';
    pill(c,n.x,n.y+r+22,n.label,labelBackground,textOn(labelBackground),INK);
  }
  const T = TABS[algo];
  if(T && T.s && G.source === n.id) tag(c, n.x-r, n.y+r, 'S', '#38b764');
  if(T && T.t && G.sink === n.id) tag(c, n.x+r, n.y+r, 'T', '#b13e53');
  if(!preferences.hideLabels&&st && st.ntext && st.ntext[n.id] != null) pill(c, n.x, n.y-r-17, st.ntext[n.id], '#ffcd75', INK, INK);
  if(pulse>0.12){
    const sparkle=2+Math.round(pulse*2);
    c.globalAlpha=0.45+0.45*pulse;c.fillStyle='#ffcd75';
    c.fillRect(n.x-r-6,n.y-r-2,sparkle,sparkle);
    c.fillRect(n.x+r+3,n.y+r-4,sparkle,sparkle);
    c.fillStyle='#ffffff';c.fillRect(n.x+r+2,n.y-r-7,sparkle,sparkle);c.globalAlpha=1;
  }
  if(hovered||pulse>0)c.restore();
}

/* ---------- view ---------- */
function zoomAt(sx, sy, f){
  const ns = clamp(view.s*f, MINS, MAXS); f = ns/view.s;
  view.x = sx-(sx-view.x)*f; view.y = sy-(sy-view.y)*f; view.s = ns; draw(); saveSoon();
}
let saveT; function saveSoon(){ clearTimeout(saveT); saveT = setTimeout(save, 400); }
function fitGraphView(graph, width, height){
  if(!graph || !graph.nodes.length) return {x:width/2,y:height/2,s:1};
  let x0=Infinity,y0=Infinity,x1=-Infinity,y1=-Infinity;
  graph.nodes.forEach(node=>{x0=Math.min(x0,node.x);y0=Math.min(y0,node.y);x1=Math.max(x1,node.x);y1=Math.max(y1,node.y);});
  x0-=80;x1+=80;y0-=60;y1+=90;
  const top=88,bottom=52,availableHeight=Math.max(1,height-top-bottom);
  const scale=clamp(Math.min(width/(x1-x0),availableHeight/(y1-y0)),MINS,1.6);
  return {s:scale,x:width/2-(x0+x1)/2*scale,y:top+availableHeight/2-(y0+y1)/2*scale};
}
function setIsomorphismSplit(enabled){
  if(enabled===isoSplitView) return;
  if(enabled){
    isoPreviousView={...view};
    isoSplitView=true;
    lastActiveSide='left';
    $('#stage').classList.add('isomorphism-mode');
    resize();
    fitView();
    if(isoGraph){
      const r=$('#stage').getBoundingClientRect();
      isoView=fitGraphView(isoGraph,Math.max(1,r.width-W),H);
    }
  }else{
    isoSplitView=false;
    lastActiveSide='left';isoSelNode=null;isoEdgePreview=null;
    $('#stage').classList.remove('isomorphism-mode');
    if(isoPreviousView) view=isoPreviousView;
    isoPreviousView=null;
    resize();
  }
}
function fitView(){
  if(isoSplitView){
    if(lastActiveSide==='right'&&isoGraph){
      const r=$('#stage').getBoundingClientRect();
      isoView=fitGraphView(isoGraph,Math.max(1,r.width-W),H);
    }else view=fitGraphView(G,W,H);
    draw();save();return;
  }
  if(!G.nodes.length){ view = {x:W/2, y:H/2, s:1}; draw(); return; }
  let x0=Infinity, y0=Infinity, x1=-Infinity, y1=-Infinity;
  G.nodes.forEach(n => { x0=Math.min(x0,n.x); y0=Math.min(y0,n.y); x1=Math.max(x1,n.x); y1=Math.max(y1,n.y); });
  x0-=80; x1+=80; y0-=60; y1+=70;
  const s = clamp(Math.min(W/(x1-x0), H/(y1-y0)), MINS, 1.6);
  view.s = s; view.x = W/2-(x0+x1)/2*s; view.y = H/2-(y0+y1)/2*s; draw(); save();
}

/* ---------- pointer / touch ---------- */
function ptr(e,canvas){ const r=canvas.getBoundingClientRect();return {x:e.clientX-r.left,y:e.clientY-r.top}; }
function bindCanvas(canvas,side){
  const listen=(name,handler,options)=>canvas.addEventListener(name,e=>withCanvasSide(side,()=>handler(e)),options);
  listen('pointerdown',e=>{
    e.preventDefault();lastActiveSide=side;
    if(side==='left')setHover(null,null);
    if(side==='left'){updateBadge();updateHint();}
    try{canvas.setPointerCapture(e.pointerId);}catch(_){}
    const p=ptr(e,canvas);pointers.set(e.pointerId,p);
    if(pointers.size===2){
      const [a,b]=[...pointers.values()];
      pinch={side,d:Math.hypot(a.x-b.x,a.y-b.y)||1,cx:(a.x+b.x)/2,cy:(a.y+b.y)/2,v:{...view}};
      if(drag&&drag.undo)save();
      drag=null;return;
    }
    if(pointers.size>2)return;
    const w=toWorld(p.x,p.y),n=hitNode(w),ed=n?null:hitEdge(w);
    let type='tap';
    if(n&&(tool==='move'||tool==='node'))type='node';
    else if(ed&&tool==='bend')type='bend';
    else if(!n&&!ed)type='pan';
    drag={side,type,n,ed,w,sx:p.x,sy:p.y,lx:p.x,ly:p.y,moved:false,undo:false,offX:n?n.x-w.x:0,offY:n?n.y-w.y:0};
  });
  listen('pointermove',e=>{
    if(!pointers.has(e.pointerId)){
      if(e.pointerType!=='touch'){
        const p=ptr(e,canvas),w=toWorld(p.x,p.y),n=hitNode(w),ed=n?null:hitEdge(w);
        if(tool==='edge'&&(side==='right'?isoSelNode:selNode)!=null){
          if(side==='right')isoEdgePreview=w;else edgePreview=w;
          draw();
        }
        if(side==='left')setHover(n,ed);
      }
      return;
    }
    if(drag&&drag.side!==side)return;
    const p=ptr(e,canvas);pointers.set(e.pointerId,p);
    if(pinch&&pinch.side===side&&pointers.size>=2){
      const [a,b]=[...pointers.values()];
      const d=Math.hypot(a.x-b.x,a.y-b.y)||1,cx=(a.x+b.x)/2,cy=(a.y+b.y)/2;
      const ns=clamp(pinch.v.s*d/pinch.d,MINS,MAXS);
      const wx=(pinch.cx-pinch.v.x)/pinch.v.s,wy=(pinch.cy-pinch.v.y)/pinch.v.s;
      view.s=ns;view.x=cx-wx*ns;view.y=cy-wy*ns;draw();return;
    }
    if(!drag)return;
    if(!drag.moved&&Math.hypot(p.x-drag.sx,p.y-drag.sy)>6)drag.moved=true;
    if(!drag.moved)return;
    const w=toWorld(p.x,p.y);
    if(drag.type==='node'){
      if(!drag.undo){pushUndo();drag.undo=true;invalidateIsomorphismResult();}
      drag.n.x=w.x+drag.offX;drag.n.y=w.y+drag.offY;
    }else if(drag.type==='pan'){view.x+=p.x-drag.lx;view.y+=p.y-drag.ly;}
    else if(drag.type==='bend'){
      if(!drag.undo){pushUndo();drag.undo=true;invalidateIsomorphismResult();}
      const g=edgeGeom(drag.ed);
      if(g){let curve=(w.x-g.mx)*g.nx+(w.y-g.my)*g.ny;if(Math.abs(curve)<6)curve=0;drag.ed.curve=curve;}
    }
    drag.lx=p.x;drag.ly=p.y;draw();
  });
  const endPtr=e=>{
    if(!pointers.has(e.pointerId))return;
    pointers.delete(e.pointerId);
    if(pinch&&pinch.side===side){if(pointers.size<2){pinch=null;save();}drag=null;return;}
    if(!drag||drag.side!==side)return;
    const d=drag;drag=null;
    if(d.moved){save();return;}
    if(e.type==='pointercancel')return;
    handleTap(d);
  };
  listen('pointerup',endPtr);
  listen('pointercancel',endPtr);
  listen('pointerleave',()=>{
    if(!pointers.size){
      if(side==='right')isoEdgePreview=null;else edgePreview=null;
      if(side==='left')setHover(null,null);
      draw();
    }
  });
  listen('contextmenu',e=>e.preventDefault());
  listen('wheel',e=>{e.preventDefault();const p=ptr(e,canvas);zoomAt(p.x,p.y,Math.exp(-e.deltaY*0.0015));},{passive:false});
}
bindCanvas(cv,'left');
bindCanvas(isoCv,'right');
document.addEventListener('gesturestart', e => e.preventDefault());

function handleTap(d){
  const {n, ed, w} = d, now = Date.now();
  const key = n ? 'n'+n.id : ed ? 'e'+ed.id : 'bg';
  const dbl = (now-lastTap.t < 400 && lastTap.key === key); lastTap = {t:now, key};
  switch(tool){
    case 'move':
      if(dbl && n) renameNode(n); else if(dbl && ed) editWeight(ed);
      else if(n) toast(nodeInfo(n)); else if(ed) toast(`${edgeName(ed)} • น้ำหนัก = ${fmt(ed.w)} (แตะ 2 ครั้งเพื่อแก้)`);
      break;
    case 'node':
      if(!n && !ed) addNodeAt(w.x, w.y); else if(n && dbl) renameNode(n);
      break;
    case 'edge':
      if(!n){
        if(activeSide==='right'){isoSelNode=null;isoEdgePreview=null;}
        else{selNode=null;edgePreview=null;updateHint();}
        draw();break;
      }
      if(selNode==null||!nodeById(selNode)){selNode=n.id;}
      else{const u=selNode;selNode=null;addEdge(u,n.id);}
      if(activeSide==='right')isoEdgePreview={x:w.x,y:w.y};
      else edgePreview={x:w.x,y:w.y};
      updateHint(); draw();
      break;
    case 'edit': if(n) renameNode(n); else if(ed) editWeight(ed); break;
    case 'del': if(n) deleteNode(n); else if(ed) deleteEdge(ed); break;
    case 'style':
      if(n) showVertexPicker(n.id,activeSide);
      else if(ed) showEdgeColors(ed);
      break;
    case 'reverse':
      if(!ed)break;
      if(!G.directed){toast('กลับทิศเส้นได้เฉพาะกราฟมีทิศทาง — กดปุ่ม → ก่อน');break;}
      if(ed.u===ed.v){toast('เส้นวนกลับจุดเดิม ไม่มีทิศทางให้สลับ');break;}
      commit(()=>{[ed.u,ed.v]=[ed.v,ed.u];});
      toast('กลับทิศทางเส้นแล้ว');
      break;
    case 'bend': if(ed && ed.curve){ commit(() => { ed.curve = 0; }, false); toast('📏 ทำให้เส้นตรงแล้ว'); } break;
  }
}
function nodeInfo(n){
  const d = degreeInfo()[n.id];
  return `${n.label} (v${n.id}) • deg = ${d.deg}` + (G.directed ? ` (เข้า ${d.in} / ออก ${d.out})` : '') + ' • แตะ 2 ครั้งเพื่อเปลี่ยนชื่อ';
}

/* ---------- edit ops ---------- */
function addNodeAt(x, y){
  let id,label; commit(() => {
    id = G.nextId++;
    const selected=vertexOptions.find(option=>option.filename===preferences.defaultVertexImage);
    label=selected?selected.name:`v${id}`;
    G.nodes.push({id,x,y,label,color:null,...(selected?{vertexImage:selected.filename}:{})});
  });
  toast(`➕ เพิ่ม ${label} แล้ว`);
}
async function showVertexPicker(nodeId,side=activeSide){
  let options;
  try{options=await loadVertexOptions();}
  catch(error){console.error('Could not load vertex images:',error);return toast(`เปิดรายการภาพไม่ได้: ${error.message}`);}
  const choices=[`<button type="button" class="btn vertex-option" data-vertex-choice=""><span>◻</span><b>ไม่ใช้ภาพ</b></button>`,
    ...options.map(option=>`<button type="button" class="btn vertex-option" data-vertex-choice="${esc(option.filename)}" data-vertex-name="${esc(option.name)}"><img loading="lazy" src="${esc(option.url)}" alt=""><b>${esc(option.name)}</b></button>`)];
  const colors=PALETTE.map((color,index)=>`<button type="button" class="btn" data-vertex-color="${index}" style="background:${color}">สี ${index+1}</button>`).join('');
  openModal('🎨 สีและรูปแบบจุดยอด',`<h3>สีจุดยอด</h3><div class="pgrid">${colors}<button type="button" class="btn" data-vertex-color="-1">ล้างสี</button></div><h3>ภาพจุดยอด</h3><p>เลือก PNG โปร่งใสจากโฟลเดอร์ vertex — ชื่อไฟล์จะกลายเป็นชื่อจุด</p><div class="vertex-grid">${choices.join('')}</div>`);
  $('#mbody').dataset.vertexNode=String(nodeId);
  $('#mbody').dataset.vertexSide=side;
}
function askWeight(def, msg){
  for(;;){
    const s = prompt(msg, String(def)); if(s === null) return null;
    const t = String(s).trim().replace(',', '.'), v = Number(t);
    if(t !== '' && isFinite(v)) return v;
    alert('⚠ น้ำหนักต้องเป็นตัวเลข เช่น 5, 2.5 หรือ -3');
  }
}
function addEdge(u, v){
  const w = askWeight(1, `น้ำหนักของเส้น ${nm(u)} ${G.directed?'→':'–'} ${nm(v)}\n(รองรับจำนวนเต็ม ทศนิยม และค่าติดลบ)`);
  if(w === null) return;
  commit(() => storeEdge(u, v, w));
  toast(`🔗 สร้างเส้น ${nm(u)} ${G.directed?'→':'–'} ${nm(v)} = ${fmt(w)}`);
}
function storeEdge(u, v, w){
  const e = {id:G.nextEid++, u, v, w, color:null, surface:'plain', curve:0};
  G.edges.push(e);
  const group=G.edges.filter(edge=>edge.u===u&&edge.v===v||edge.u===v&&edge.v===u).sort((a,b)=>a.id-b.id);
  if(group.length<2)return;
  group.forEach((edge,index)=>{
    const canonicalCurve=(index-(group.length-1)/2)*PARALLEL_CURVE_GAP;
    edge.curve=canonicalCurve*(edge.u<=edge.v?1:-1);
  });
}
function renameNode(n){
  const s = prompt('ตั้งชื่อจุดยอด (เช่น คลังสินค้า, ร้านค้า 1, โรงพยาบาล):', n.label);
  if(s === null) return;
  const t = s.trim() || ('v'+n.id);
  commit(() => { n.label = t; }, false);
}
function editWeight(e){
  const w = askWeight(e.w, `น้ำหนักใหม่ของเส้น ${edgeName(e)}:`);
  if(w === null) return;
  commit(() => { e.w = w; });
}
function showEdgeColors(edge){
  openModal(`🎨 สีและรูปแบบเส้น ${edgeName(edge)}`,
    `<h3>สีเส้น</h3><p>เลือกสีเส้นแบบกำหนดเอง</p><div class="pgrid">`+
    PALETTE.map((color,index)=>`<button type="button" class="btn" data-edge-color="${index}" style="background:${color}">สี ${index+1}</button>`).join('')+
    `<button type="button" class="btn" data-edge-color="-1">ล้างสี</button></div><h3>รูปแบบสำเร็จรูป</h3><p>เลือกชนิดโครงสร้างเพื่อแสดงเส้นเป็นรูปแบบเฉพาะ</p><div class="pgrid">`+
    Object.entries(EDGE_SURFACES).map(([surface,label])=>`<button type="button" class="btn ${edge.surface===surface?'on':''}" data-edge-surface="${surface}">${({plain:'➖',road:'🛣️',water:'🚰',power:'⚡',gas:'🟡',rail:'🚆',fiber:'📡',sewer:'🕳️'})[surface]} ${label}</button>`).join('')+
    `</div><p class="note">แตะเส้นเพื่อใช้รูปแบบกับเส้นนั้น สีและรูปแบบแสดงในกราฟและภาพส่งออก</p>`);
  $('#mbody').dataset.edgeId=String(edge.id);
  $('#mbody').dataset.edgeSide=activeSide;
}
function deleteNode(n){
  commit(() => {
    G.edges = G.edges.filter(e => e.u !== n.id && e.v !== n.id);
    G.nodes = G.nodes.filter(x => x !== n);
    if(G.source === n.id) G.source = null; if(G.sink === n.id) G.sink = null; if(selNode === n.id) selNode = null;
  });
  toast(`🗑 ลบ ${n.label} แล้ว`);
}
function deleteEdge(e){ commit(() => { G.edges = G.edges.filter(x => x !== e); }); toast(`🗑 ลบเส้น ${edgeName(e)} แล้ว`); }

/* ---------- graph helpers ---------- */
function outAdj(){
  const adj = new Map(G.nodes.map(n => [n.id, []]));
  for(const e of G.edges){ adj.get(e.u).push({to:e.v, w:e.w, e}); if(!G.directed) adj.get(e.v).push({to:e.u, w:e.w, e}); }
  return adj;
}
function nbrSets(){
  const m = new Map(G.nodes.map(n => [n.id, new Set()]));
  for(const e of G.edges){ if(e.u === e.v) continue; m.get(e.u).add(e.v); m.get(e.v).add(e.u); }
  return m;
}
function components(){
  const nb = nbrSets(), seen = new Set(), comps = [];
  for(const n of G.nodes){
    if(seen.has(n.id)) continue;
    const comp = [], q = [n.id]; seen.add(n.id);
    while(q.length){ const u = q.shift(); comp.push(u); for(const v of nb.get(u)) if(!seen.has(v)){ seen.add(v); q.push(v); } }
    comps.push(comp);
  }
  return comps;
}
function degreeInfo(){
  const d = {}; G.nodes.forEach(n => d[n.id] = {deg:0, in:0, out:0});
  G.edges.forEach(e => { d[e.u].deg++; d[e.v].deg++; d[e.u].out++; d[e.v].in++; });
  return d;
}
function isBipartite(){
  const color=new Map(),adj=nbrSets();
  for(const n of G.nodes)if(!color.has(n.id)){
    color.set(n.id,0);const q=[n.id];
    while(q.length){const u=q.shift();for(const v of adj.get(u)){if(!color.has(v)){color.set(v,1-color.get(u));q.push(v);}else if(color.get(v)===color.get(u))return false;}}
  }
  return !G.edges.some(e=>e.u===e.v);
}
function isDAG(){
  if(!G.directed)return false;
  const indeg=new Map(G.nodes.map(n=>[n.id,0])),adj=new Map(G.nodes.map(n=>[n.id,[]]));
  for(const e of G.edges){adj.get(e.u).push(e.v);indeg.set(e.v,indeg.get(e.v)+1);}
  const q=G.nodes.filter(n=>indeg.get(n.id)===0).map(n=>n.id);let visited=0;
  while(q.length){const u=q.shift();visited++;for(const v of adj.get(u)){indeg.set(v,indeg.get(v)-1);if(indeg.get(v)===0)q.push(v);}}
  return visited===G.nodes.length;
}
function isStronglyConnected(){
  if(!G.directed||!G.nodes.length)return false;
  const reach=start=>{
    const adj=new Map(G.nodes.map(n=>[n.id,[]]));
    for(const e of G.edges)adj.get(start===-1?e.v:e.u).push(start===-1?e.u:e.v);
    const seen=new Set([G.nodes[0].id]),q=[G.nodes[0].id];
    while(q.length){for(const v of adj.get(q.shift()))if(!seen.has(v)){seen.add(v);q.push(v);}}
    return seen.size===G.nodes.length;
  };
  return reach(1)&&reach(-1);
}
function graphMetrics(){
  const ids=G.nodes.map(n=>n.id),adj=outAdj(),n=ids.length;
  const distances=new Map(),ecc=new Map(),degreeCent=new Map(),closeness=new Map(),betweenness=new Map(),clustering=new Map();
  for(const source of ids){
    const dist=new Map([[source,0]]),q=[source];
    while(q.length){const u=q.shift();for(const a of adj.get(u))if(!dist.has(a.to)){dist.set(a.to,dist.get(u)+1);q.push(a.to);}}
    distances.set(source,dist);
    ecc.set(source,dist.size===n?Math.max(0,...dist.values()):Infinity);
    const sum=[...dist.values()].reduce((a,b)=>a+b,0);
    closeness.set(source,n>1&&sum>0?(dist.size-1)/sum:0);
    const neighbors=nbrSets().get(source),k=neighbors.size;
    let links=0;for(const u of neighbors)for(const v of neighbors)if(u<v&&nbrSets().get(u).has(v))links++;
    clustering.set(source,k<2?0:2*links/(k*(k-1)));
    degreeCent.set(source,n>1?neighbors.size/(n-1):0);
  }
  if(n<=500){
    const centralAdj=new Map(ids.map(id=>[id,adj.get(id).map(a=>a.to)]));
    for(const source of ids){
      const stack=[],pred=new Map(ids.map(id=>[id,[]])),sigma=new Map(ids.map(id=>[id,0])),dist=new Map(ids.map(id=>[id,-1]));
      sigma.set(source,1);dist.set(source,0);const q=[source];
      while(q.length){const v=q.shift();stack.push(v);for(const w of centralAdj.get(v)){
        if(dist.get(w)<0){dist.set(w,dist.get(v)+1);q.push(w);}
        if(dist.get(w)===dist.get(v)+1){sigma.set(w,sigma.get(w)+sigma.get(v));pred.get(w).push(v);}
      }}
      const delta=new Map(ids.map(id=>[id,0]));
      while(stack.length){const w=stack.pop();for(const v of pred.get(w))if(sigma.get(w))delta.set(v,delta.get(v)+sigma.get(v)/sigma.get(w)*(1+delta.get(w)));if(w!==source)betweenness.set(w,(betweenness.get(w)||0)+delta.get(w));}
    }
    const scale=G.directed?((n-1)*(n-2)):((n-1)*(n-2)/2);
    if(scale>0)for(const id of ids)betweenness.set(id,(betweenness.get(id)||0)/(scale*(G.directed?1:2)));
    else for(const id of ids)betweenness.set(id,0);
  }
  let girth=Infinity;
  if(!G.directed){
    for(const e of G.edges)if(e.u===e.v)girth=1;
    const pairs=new Map();
    for(const e of G.edges)if(e.u!==e.v){const key=`${Math.min(e.u,e.v)}:${Math.max(e.u,e.v)}`;pairs.set(key,(pairs.get(key)||0)+1);}
    for(const count of pairs.values())if(count>1)girth=Math.min(girth,2);
    const simpleAdj=new Map(ids.map(id=>[id,[]]));
    for(const e of G.edges)if(e.u!==e.v){simpleAdj.get(e.u).push([e.v,e.id]);simpleAdj.get(e.v).push([e.u,e.id]);}
    for(const source of ids){
      const dist=new Map([[source,0]]),parentEdge=new Map(),q=[source];
      while(q.length){const u=q.shift();for(const [v,eid] of simpleAdj.get(u)){
        if(!dist.has(v)){dist.set(v,dist.get(u)+1);parentEdge.set(v,eid);q.push(v);}
        else if(parentEdge.get(u)!==eid&&parentEdge.get(v)!==eid)girth=Math.min(girth,dist.get(u)+dist.get(v)+1);
      }}
    }
  }
  const connected=n>0&&(G.directed?isStronglyConnected():components().length===1);
  return {ecc,degreeCent,closeness,betweenness,clustering,girth,connected,
    radius:connected?Math.min(...ecc.values()):Infinity,
    diameter:connected?Math.max(...ecc.values()):Infinity,
    center:connected?ids.filter(id=>ecc.get(id)===Math.min(...ecc.values())):[],
    periphery:connected?ids.filter(id=>ecc.get(id)===Math.max(...ecc.values())):[]};
}
function mkStep(msg, b, ex){
  ex = ex || {};
  return {msg, ntext:ex.ntext||b.ntext||null, node:Object.assign({}, b.node, ex.node), edge:Object.assign({}, b.edge, ex.edge), etext:ex.etext||b.etext||null, fill:ex.fill||b.fill||null};
}

/* ---------- analysis ---------- */
function matrixHTML(kind){
  const ids = G.nodes.map(n => n.id), idx = new Map(ids.map((id,i) => [id,i]));
  const A = ids.map(() => ids.map(() => 0)), M = ids.map(() => ids.map(() => null));
  for(const e of G.edges){
    const i = idx.get(e.u), j = idx.get(e.v);
    A[i][j]++; M[i][j] = M[i][j] == null ? e.w : Math.min(M[i][j], e.w);
    if(!G.directed){ A[j][i]++; M[j][i] = M[i][j]; }
  }
  let h = '<div class="tw"><table class="tbl"><tr><th></th>' + ids.map(id => `<th title="${esc(nm(id))}">v${id}</th>`).join('') + '</tr>';
  ids.forEach((id,i) => {
    h += `<tr><th title="${esc(nm(id))}">v${id}</th>` + ids.map((_,j) => {
      if(kind === 'A') return `<td>${A[i][j]}</td>`;
      return `<td>${i===j ? 0 : (M[i][j] == null ? '∞' : fmt(M[i][j]))}</td>`;
    }).join('') + '</tr>';
  });
  return h + '</table></div>';
}
function analysisHTML(){
  const n = G.nodes.length, m = G.edges.length, deg = degreeInfo(), comps = components();
  const sumDeg = G.nodes.reduce((a,x) => a+deg[x.id].deg, 0), neg = G.edges.filter(e => e.w < 0);
  const loops=G.edges.filter(e=>e.u===e.v).length, keys=new Set(),parallel=G.edges.reduce((a,e)=>{
    const k=G.directed?`${e.u}>${e.v}`:`${Math.min(e.u,e.v)}-${Math.max(e.u,e.v)}`;
    if(keys.has(k))return a+1;keys.add(k);return a;
  },0);
  const simple=!loops&&!parallel, maxEdges=G.directed?n*(n-1):n*(n-1)/2;
  const density=maxEdges?m/maxEdges:0, tree=!G.directed&&simple&&n>0&&comps.length===1&&m===n-1;
  const complete=simple&&m===maxEdges, bipartite=isBipartite();
  const degreeSeq=G.nodes.map(x=>deg[x.id].deg).sort((a,b)=>b-a);
  const weightSum=G.edges.reduce((a,e)=>a+e.w,0);
  let h = `<div class="cards">${card('|V| จำนวนจุดยอด', n)}${card('|E| จำนวนเส้นเชื่อม', m)}${card('ชนิดกราฟ', G.directed?'มีทิศทาง →':'ไม่มีทิศทาง —')}${card('Components', comps.length)}</div>`;
  if(!n) return h + '<div class="hero warn">ยังไม่มีจุดยอด ลองกด 📂 ตัวอย่าง หรือ ⬛ เพิ่มจุด</div>';
  h += `<h3>คุณสมบัติ</h3><div class="cards">${card('Simple',simple?'ใช่':'ไม่ใช่')}${card('Self-loop',loops)}${card('เส้นขนานเพิ่มเติม',parallel)}${card('Complete',complete?'ใช่':'ไม่ใช่')}${card('Bipartite',bipartite?'ใช่':'ไม่ใช่')}${card('Tree',tree?'ใช่':'ไม่ใช่')}${card('DAG',isDAG()?'ใช่':'ไม่ใช่')}${card('Strongly Connected',isStronglyConnected()?'ใช่':'ไม่ใช่')}${card('Density',density.toFixed(3))}${card('ผลรวมน้ำหนัก',fmt(weightSum))}</div>`;
  h += `<p><b>Degree Sequence:</b> (${degreeSeq.join(', ')})</p>`;
  const metrics=graphMetrics();
  h += `<h3>ระยะทางและโครงสร้าง</h3><div class="cards">${card('Girth',metrics.girth===Infinity?'ไม่มีวงจร':metrics.girth)}${card('Radius',metrics.connected?fmt(metrics.radius):'กราฟไม่เชื่อมต่อ')}${card('Diameter',metrics.connected?fmt(metrics.diameter):'กราฟไม่เชื่อมต่อ')}${card('Center',metrics.center.map(id=>esc(nm(id))).join(', ') || '—')}${card('Periphery',metrics.periphery.map(id=>esc(nm(id))).join(', ') || '—')}</div>`;
  if(n<=500){
    h += '<div class="tw"><table class="tbl"><tr><th>จุด</th><th>Degree</th><th>Closeness</th><th>Betweenness</th><th>Clustering</th></tr>';
    for(const node of G.nodes)h+=`<tr><td>${esc(nm(node.id))}</td><td>${fmt(metrics.degreeCent.get(node.id))}</td><td>${fmt(metrics.closeness.get(node.id))}</td><td>${fmt(metrics.betweenness.get(node.id)||0)}</td><td>${fmt(metrics.clustering.get(node.id))}</td></tr>`;
    h += '</table></div>';
  }else h += '<p>คำนวณ Centrality เมื่อ |V| ≤ 500</p>';
  h += comps.length <= 1
    ? `<div class="hero">✔ กราฟเชื่อมต่อกัน (Connected)${G.directed?' แบบไม่สนทิศ':''} — Prim จะได้ Spanning Tree เดียว</div>`
    : `<div class="hero warn">⚠ กราฟไม่เชื่อมต่อ มี ${comps.length} ส่วน — Prim จะได้ Spanning Forest และ Flow/Dijkstra อาจไปไม่ถึงบางจุด</div>`;
  h += `<h3>ตรวจ Σdeg = 2|E|</h3><p>Σdeg = ${G.nodes.map(x => deg[x.id].deg).join(' + ')} = <b>${sumDeg}</b> และ 2|E| = 2 × ${m} = <b>${2*m}</b> ${sumDeg===2*m?'✔ ถูกต้อง':'✘'}</p>`;
  if(G.directed) h += `<p>กราฟมีทิศ: Σdeg⁺(ออก) = ${G.nodes.reduce((a,x)=>a+deg[x.id].out,0)} = Σdeg⁻(เข้า) = ${G.nodes.reduce((a,x)=>a+deg[x.id].in,0)} = |E| ✔</p>`;
  h += `<h3>ตรวจน้ำหนักติดลบ</h3>` + (neg.length ? `<div class="hero bad">⚠ พบ ${neg.length} เส้นติดลบ: ${neg.map(e => esc(edgeName(e))).join(', ')} — ห้ามใช้ Dijkstra</div>` : '<p>✔ ไม่มีน้ำหนักติดลบ (Dijkstra ใช้ได้)</p>');
  h += `<h3>Degree ของแต่ละจุด</h3><div class="tw"><table class="tbl"><tr><th>จุด</th><th>ชื่อ</th><th>deg</th>${G.directed?'<th>เข้า (in)</th><th>ออก (out)</th>':''}</tr>`;
  G.nodes.forEach(x => { h += `<tr><td>v${x.id}</td><td class="l">${esc(x.label)}</td><td><b>${deg[x.id].deg}</b></td>${G.directed?`<td>${deg[x.id].in}</td><td>${deg[x.id].out}</td>`:''}</tr>`; });
  h += '</table></div>';
  h += `<h3>Components (${comps.length})</h3>` + comps.map((c,i) => `<div>ส่วนที่ ${i+1}: ${c.map(id => `<span class="chip">${esc(nm(id))}</span>`).join('')}</div>`).join('');
  if(n <= 30){
    h += `<h3>Adjacency Matrix</h3><p style="font-size:13px">แถว = ต้นทาง, คอลัมน์ = ปลายทาง, ตัวเลข = จำนวนเส้น</p>` + matrixHTML('A');
    h += `<h3>Weight Matrix</h3><p style="font-size:13px">∞ = ไม่มีเส้นตรงถึงกัน (ถ้ามีหลายเส้นจะใช้ค่าน้อยสุด)</p>` + matrixHTML('W');
    const ids=G.nodes.map(x=>x.id), adj=outAdj();
    h += '<h3>Adjacency List</h3><div class="tw"><table class="tbl"><tr><th>จุด</th><th class="l">เพื่อนบ้าน (น้ำหนัก)</th></tr>';
    for(const id of ids) h += `<tr><th>${esc(nm(id))}</th><td class="l">${adj.get(id).map(a=>`${esc(nm(a.to))} (${fmt(a.w)})`).join(', ') || '—'}</td></tr>`;
    h += '</table></div>';
    h += '<h3>Incidence Matrix</h3><p style="font-size:13px">คอลัมน์ e = เส้นเชื่อม; loop ในกราฟไม่มีทิศใช้ค่า 2</p><div class="tw"><table class="tbl"><tr><th></th>';
    h += G.edges.map((e,i)=>`<th title="${esc(edgeName(e))}">e${i+1}</th>`).join('')+'</tr>';
    for(const id of ids){
      h += `<tr><th title="${esc(nm(id))}">${esc(nm(id))}</th>`;
      h += G.edges.map(e=>{
        let value=0;
        if(G.directed){if(e.u===id)value--;if(e.v===id)value++;}
        else if(e.u===id&&e.v===id)value=2;
        else if(e.u===id||e.v===id)value=1;
        return `<td>${value}</td>`;
      }).join('')+'</tr>';
    }
    h += '</table></div>';
    const dist=ids.map(()=>ids.map(()=>Infinity));
    ids.forEach((id,i)=>{dist[i][i]=0;const q=[id];while(q.length){const u=q.shift(),ui=ids.indexOf(u);for(const a of adj.get(u))if(dist[i][ids.indexOf(a.to)]===Infinity){dist[i][ids.indexOf(a.to)]=dist[i][ui]+1;q.push(a.to);}}});
    h += '<h3>Distance Matrix (จำนวนเส้น)</h3><div class="tw"><table class="tbl"><tr><th></th>'+ids.map(id=>`<th title="${esc(nm(id))}">${esc(nm(id))}</th>`).join('')+'</tr>';
    ids.forEach((id,i)=>{h+=`<tr><th title="${esc(nm(id))}">${esc(nm(id))}</th>`+dist[i].map(v=>`<td>${v===Infinity?'∞':v}</td>`).join('')+'</tr>';});
    h += '</table></div>';
    const reach=ids.map((_,i)=>dist[i].map(v=>v<Infinity));
    h += '<h3>Reachability Matrix (Transitive Closure)</h3><div class="tw"><table class="tbl"><tr><th></th>'+ids.map(id=>`<th title="${esc(nm(id))}">${esc(nm(id))}</th>`).join('')+'</tr>';
    ids.forEach((id,i)=>{h+=`<tr><th title="${esc(nm(id))}">${esc(nm(id))}</th>`+reach[i].map(v=>`<td>${v?'1':'0'}</td>`).join('')+'</tr>';});
    h += '</table></div>';
  } else h += '<p>(Matrix แสดงเมื่อ |V| ≤ 30)</p>';
  return h;
}
function showAnalysis(){ openModal('🔍 ผลวิเคราะห์กราฟ', analysisHTML()); }

/* ---------- Python algorithm API ---------- */
async function runPythonAlgorithm(algorithm, extra = {}){
  if(!G.nodes.length && algorithm !== 'havelhakimi') return toast('ยังไม่มีจุดยอด');
  try{
    const response = await fetch('/api/run', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({
        algorithm,
        nodes:G.nodes.map(({id,label}) => ({id,label})),
        edges:G.edges.map(({id,u,v,w}) => ({id,u,v,w})),
        directed:G.directed,
        source:G.source,
        sink:G.sink,
        colorNames:G.colorNames,
        ...extra
      })
    });
    const result = await response.json();
    if(!response.ok) throw new Error(result.error || `HTTP ${response.status}`);
    if(result.key==='planarity'){
      if(result.planar===true&&result.planarLayout)preparePlanarityAnimation(result.planarLayout);
      else resetPlanarityAnimation();
    }
    if(result.key === 'pruferDecode' || result.key === 'graphTransform' || (result.key === 'degreeSequence' && result.exists)){
      pushUndo();
      const center = toWorld(W/2, H/2), radius = Math.max(90, result.nodes.length * 18);
      G = emptyGraph();
      G.directed = !!result.directed;
      G.nodes = result.nodes.map((node, index) => {
        const angle = 2*Math.PI*index/result.nodes.length - Math.PI/2;
        return {...node, x:center.x+radius*Math.cos(angle), y:center.y+radius*Math.sin(angle), color:null};
      });
      G.edges = result.edges.map(edge => ({...edge, curve:0, color:null}));
      G.nextId = G.nodes.length + 1;
      G.nextEid = G.edges.length + 1;
      afterChange();
      fitView();
    } else if(result.key === 'color'){
      pushUndo();
      G.nodes.forEach(n => { n.color = result.colors[n.id] ?? null; });
      save();
    } else if(result.key === 'edgeColor'){
      pushUndo();
      G.edges.forEach(edge => { edge.color = result.colors[edge.id] ?? null; });
      save();
    } else if(result.key === 'bipartite' && result.isBipartite){
      pushUndo();
      G.nodes.forEach(node => { node.color = result.colors[node.id] ?? null; });
      save();
    } else if(result.key === 'isomorphism'){
      displayIsomorphismComparison(extra.otherGraph, result);
    }
    setRun({
      key:result.key,
      title:result.title,
      steps:result.key === 'isomorphism' && result.isomorphic ? isomorphismAnimationSteps() :
        result.key === 'planarity' && result.planar === true && result.planarLayout ? planarityAnimationSteps() : result.steps,
      summary:() => result.summary.replace(/\{\{COLOR_NAME_(\d+)\}\}/g, (_, i) => esc(cName(+i))) +
        (result.key === 'isomorphism' && result.isomorphic ? isomorphismMappingSummary() : '')
    });
  }catch(error){
    console.error('Python algorithm request failed:', error);
    toast(`รันอัลกอริทึมไม่สำเร็จ: ${error.message}`);
  }
}
function displayIsomorphismComparison(otherGraph,result){
  isoGraph = JSON.parse(JSON.stringify(otherGraph));
  const nodeCount=isoGraph.nodes.length, radius=Math.min(240,Math.max(90,nodeCount*24));
  isoGraph.nodes=isoGraph.nodes.map((node,index)=>{
    const angle=2*Math.PI*index/nodeCount-Math.PI/2;
    return {...node,x:400+radius*Math.cos(angle),y:300+radius*Math.sin(angle),color:null};
  });
  isoGraph.nextId=Math.max(1,...isoGraph.nodes.map(node=>node.id+1));
  isoGraph.nextEid=Math.max(1,...isoGraph.edges.map(edge=>edge.id+1));
  isoFirstGraph=JSON.parse(JSON.stringify(G));
  isoMapping=result.isomorphic ? result.mapping : null;
  isoColors=[];isoEdgePairs=[];
  $('#isoMappingLegend').replaceChildren();
  if(isoMapping){
    const leftById=new Map(isoFirstGraph.nodes.map(node=>[String(node.id),node]));
    const rightById=new Map(isoGraph.nodes.map(node=>[String(node.id),node]));
    const colorByLeft=new Map();
    for(const [index,[leftId,rightId]] of Object.entries(isoMapping).entries()){
      const left=leftById.get(String(leftId)),right=rightById.get(String(rightId));
      if(!left||!right) continue;
      const colorIndex=index%PALETTE.length,color=PALETTE[colorIndex];
      left.color=colorIndex;right.color=colorIndex;colorByLeft.set(String(leftId),colorIndex);
      isoColors.push({leftId:String(leftId),rightId:String(rightId),leftLabel:left.label,rightLabel:right.label,color});
    }
    const rightEdgeByPair=new Map();
    const pairKey=(u,v)=>isoGraph.directed?`${u}>${v}`:`${Math.min(u,v)}-${Math.max(u,v)}`;
    isoGraph.edges.forEach(edge=>rightEdgeByPair.set(pairKey(edge.u,edge.v),edge));
    for(const [edgeIndex,edge] of isoFirstGraph.edges.entries()){
      const mappedU=isoMapping[String(edge.u)],mappedV=isoMapping[String(edge.v)];
      const matching=rightEdgeByPair.get(pairKey(mappedU,mappedV));
      if(!matching) continue;
      const colorIndex=(edgeIndex+isoColors.length)%PALETTE.length;
      isoEdgePairs.push({leftId:edge.id,rightId:matching.id,color:PALETTE[colorIndex]});
    }
    $('#isoMappingLegend').innerHTML=isoColors.map(pair=>
      `<span class="iso-pair-chip"><i style="background:${pair.color}"></i>${esc(pair.leftLabel)} → ${esc(pair.rightLabel)}</span>`
    ).join('');
    $('#isoMappingLegend').classList.add('visible');
    $('#isoRightStatus').textContent='Isomorphic ✓ สีเดียวกันแสดงคู่จุดยอดที่ตรงกัน';
  }else{
    $('#isoMappingLegend').classList.remove('visible');
    $('#isoRightStatus').textContent='ไม่ Isomorphic — ไม่พบการจับคู่ที่รักษาเส้นเชื่อม';
  }
  const stageRect=$('#stage').getBoundingClientRect();
  isoView=fitGraphView(isoGraph,Math.max(1,stageRect.width-W),H);
  if(isoMapping){
    const leftById=new Map(isoFirstGraph.nodes.map(node=>[String(node.id),node]));
    isoAnimation={frame:0,initial:new Map(),targets:new Map()};
    for(const node of isoGraph.nodes) isoAnimation.initial.set(String(node.id),{x:node.x,y:node.y});
    for(const pair of isoColors){
      const left=leftById.get(pair.leftId);
      if(!left) continue;
      isoAnimation.targets.set(pair.rightId,{
        x:(view.x+left.x*view.s-isoView.x)/isoView.s,
        y:(view.y+left.y*view.s-isoView.y)/isoView.s
      });
    }
  }else isoAnimation=null;
  draw();
}
function isomorphismAnimationSteps(){
  return [
    {msg:'เริ่มต้น: กราฟที่สองยังอยู่ในตำแหน่งเดิม'},
    ...isoColors.map((pair,index)=>({msg:`จับคู่จุด ${pair.rightLabel} ↔ ${pair.leftLabel} (${index+1}/${isoColors.length})`})),
    ...isoEdgePairs.map((pair,index)=>({msg:`จับคู่เส้น e${pair.rightId} ↔ e${pair.leftId} (${index+1}/${isoEdgePairs.length})`}))
  ];
}
function animateIsomorphismTo(index){
  if(!isoAnimation||!isoGraph||algo!=='isomorphism') return;
  if(isoAnimation.frame) cancelAnimationFrame(isoAnimation.frame);
  const matched=new Set(isoColors.slice(0,clamp(index,0,isoColors.length)).map(pair=>pair.rightId));
  const starts=new Map(),destinations=new Map();
  isoGraph.nodes.forEach(node=>{
    const id=String(node.id),target=matched.has(id)?isoAnimation.targets.get(id):isoAnimation.initial.get(id);
    if(target){starts.set(id,{x:node.x,y:node.y});destinations.set(id,target);}
  });
  const startTime=performance.now(),duration=420;
  const frame=now=>{
    if(!isoAnimation) return;
    const progress=clamp((now-startTime)/duration,0,1),eased=1-Math.pow(1-progress,3);
    isoGraph.nodes.forEach(node=>{
      const id=String(node.id),from=starts.get(id),to=destinations.get(id);
      if(from&&to){node.x=from.x+(to.x-from.x)*eased;node.y=from.y+(to.y-from.y)*eased;}
    });
    draw();
    if(progress<1) isoAnimation.frame=requestAnimationFrame(frame);
    else isoAnimation.frame=0;
  };
  isoAnimation.frame=requestAnimationFrame(frame);
}
function invalidateIsomorphismResult(){
  if(!isoFirstGraph&&!isoMapping&&!isoColors.length)return;
  clearRun();
  if(isoAnimation&&isoAnimation.frame) cancelAnimationFrame(isoAnimation.frame);
  isoAnimation=null;
  isoFirstGraph=null;isoMapping=null;isoColors=[];
  if(isoGraph){
    isoGraph.nodes.forEach(node=>{if(node.color!=null)node.color=null;});
    isoGraph.edges.forEach(edge=>{if(edge.color!=null)edge.color=null;});
  }
  const legend=$('#isoMappingLegend');
  if(legend){legend.replaceChildren();legend.classList.remove('visible');}
  const status=$('#isoRightStatus');
  if(status)status.textContent=`กราฟที่สองมี ${isoGraph?isoGraph.nodes.length:0} จุด • ${isoGraph?isoGraph.edges.length:0} เส้น — แก้ไขได้ด้วยเครื่องมือด้านบน`;
}
function isomorphismMappingSummary(){
  if(!isoColors.length) return '';
  const rows=isoColors.map(pair=>
    `<tr><td><span class="sw" style="background:${pair.color}"></span>${esc(pair.leftLabel)}</td><td>→</td><td><span class="sw" style="background:${pair.color}"></span>${esc(pair.rightLabel)}</td></tr>`
  ).join('');
  return `<h3>จุดยอดที่จับคู่กัน</h3><div class="tw"><table class="tbl"><tr><th>กราฟที่ 1</th><th></th><th>กราฟที่ 2</th></tr>${rows}</table></div>`;
}
function runDijkstra(){ return runPythonAlgorithm('dijkstra'); }
function runPrim(){ return runPythonAlgorithm('prim'); }
function runKruskal(){ return runPythonAlgorithm('kruskal'); }
function runEuler(){ return runPythonAlgorithm('euler'); }
function runEdgeColoring(){ return runPythonAlgorithm('edgecolor'); }
function runColoring(){ return runPythonAlgorithm('color'); }
function runFlow(){ return runPythonAlgorithm('flow'); }
function runHamiltonian(){ return runPythonAlgorithm('hamiltonian'); }
function runPlanarity(){ return runPythonAlgorithm('planarity'); }
function runVertexConnectivity(){ return runPythonAlgorithm('vertexconnectivity'); }
function runEdgeConnectivity(){ return runPythonAlgorithm('edgeconnectivity'); }
function showDegreeSequenceInput(initial=''){
  openModal('📊 Degree Sequence', `
    <p>ใส่ Degree ของแต่ละจุดยอด คั่นด้วยช่องว่างหรือจุลภาค เช่น <b>3, 2, 2, 1</b></p>
    <label>Degree Sequence
      <input id="degreeSequenceInput" type="text" inputmode="numeric" autocomplete="off" placeholder="เช่น 3, 2, 2, 1" value="${esc(initial)}">
    </label>
    <p><button type="button" class="btn primary" id="buildDegreeSequence">ตรวจสอบและสร้างกราฟ</button></p>
    <p class="note">ใช้ Havel–Hakimi และ Erdős–Gallai ตรวจว่าลำดับนี้สร้างเป็นกราฟอย่างง่ายได้หรือไม่ (1–500 จุดยอด)</p>`);
  $('#degreeSequenceInput').focus();
}
function runDegreeSequenceFromInput(){
  const raw = $('#degreeSequenceInput').value.trim();
  if(!raw) return toast('กรุณาใส่ Degree Sequence');
  const tokens = raw.split(/[,\s]+/);
  if(tokens.some(token => !/^\d+$/.test(token))) return toast('Degree ต้องเป็นจำนวนเต็มไม่ติดลบ คั่นด้วยช่องว่างหรือจุลภาค');
  const degreeSequence = tokens.map(Number);
  if(degreeSequence.some(value => !Number.isSafeInteger(value))) return toast('มี Degree ที่มีค่ามากเกินไป');
  closeModal();
  return runPythonAlgorithm('havelhakimi', {degreeSequence});
}
function runComplement(){ return runPythonAlgorithm('transform', {operation:'complement'}); }
function runBipartite(){ return runPythonAlgorithm('bipartite'); }
function showIsomorphismInput(){
  const presetOptions = Object.entries(PRESETS)
    .map(([key, preset]) => `<option value="${key}">${esc(preset.name)}</option>`).join('');
  const drawnOption=isoGraph&&isoGraph.nodes.length?`<option value="drawn" selected>ใช้กราฟที่วาดไว้ทางขวา (${isoGraph.nodes.length} จุด, ${isoGraph.edges.length} เส้น)</option>`:'';
  openModal('🔁 Isomorphic Graphs', `<p>สร้างหรือแก้กราฟได้ทั้งสองฝั่ง แล้วเลือกเปรียบเทียบกราฟที่วาดไว้ทางขวา หรือนำเข้าตัวอย่าง/Edge List</p>
    <div class="row"><label class="sel">กราฟที่สอง<select id="isoPreset">${drawnOption}<option value="custom" ${drawnOption?'':'selected'}>กำหนดด้วย Edge List</option>${presetOptions}</select></label></div>
    <div class="row"><label class="sel">จำนวนจุดยอดของกราฟที่สอง <input id="isoNodeCount" type="number" min="1" max="12" value="${Math.max(1, G.nodes.length)}"></label></div>
    <label>Edge List <textarea id="isoEdges" rows="3" placeholder="${G.directed ? 'ตัวอย่างกราฟมีทิศทาง: 1&gt;2, 2&gt;3' : 'ตัวอย่างกราฟไม่มีทิศทาง: 1-2, 2-3'}"></textarea></label>
    <label><input id="isoDirected" type="checkbox" ${G.directed ? 'checked' : ''}> กราฟที่สองมีทิศทาง</label>
    <p class="note">เปรียบเทียบโครงสร้างโดยไม่สนชื่อจุดยอดหรือน้ำหนัก รองรับกราฟอย่างง่ายไม่เกิน 12 จุดยอด (ไม่มี self-loop/เส้นขนาน)</p>
    <p><button type="button" class="btn primary" id="runIsomorphismCompare">เปรียบเทียบกราฟ</button></p>`);
}
function runIsomorphismComparison(){
  let otherGraph;
  const presetKey = $('#isoPreset').value;
  if(presetKey==='drawn'){
    if(!isoGraph||!isoGraph.nodes.length)return toast('เพิ่มจุดยอดทางฝั่งขวาก่อนเปรียบเทียบ');
    otherGraph={
      nodes:isoGraph.nodes.map(({id,label})=>({id,label})),
      edges:isoGraph.edges.map(({id,u,v,w})=>({id,u,v,w})),
      directed:isoGraph.directed
    };
  }else if(presetKey !== 'custom'){
    const preset = PRESETS[presetKey];
    if(!preset) return toast('ไม่พบตัวอย่างกราฟที่เลือก');
    const graph = preset.build();
    otherGraph = {
      nodes:graph.nodes.map(({id,label}) => ({id,label})),
      edges:graph.edges.map(({id,u,v,w}) => ({id,u,v,w})),
      directed:graph.directed
    };
  }else{
    const count = Number($('#isoNodeCount').value), directed = $('#isoDirected').checked;
    if(!Number.isInteger(count) || count < 1 || count > 12) return toast('กราฟที่สองต้องมี 1–12 จุดยอด');
    const raw = $('#isoEdges').value.trim();
    const pairs = raw ? raw.split(/[;,\n]+/).map(item => item.trim()) : [];
    const edges = [], seen = new Set();
    for(const pair of pairs){
      const match = directed ? pair.match(/^(\d+)\s*(?:>|→)\s*(\d+)$/) : pair.match(/^(\d+)\s*-\s*(\d+)$/);
      if(!match) return toast(`รูปแบบ Edge List ไม่ถูกต้อง: ${pair}`);
      const u = Number(match[1]), v = Number(match[2]);
      if(u < 1 || u > count || v < 1 || v > count || u === v) return toast(`เส้น ${pair} ต้องเชื่อมจุด 1–${count} และห้ามเป็น self-loop`);
      const key = directed ? `${u}>${v}` : `${Math.min(u,v)}-${Math.max(u,v)}`;
      if(seen.has(key)) return toast(`พบเส้นซ้ำ: ${pair}`);
      seen.add(key); edges.push({id:edges.length+1,u,v,w:1});
    }
    otherGraph = {
      nodes:Array.from({length:count},(_,index)=>({id:index+1,label:`v${index+1}`})),
      edges,
      directed
    };
    isoGraph=sanitize({
      nodes:otherGraph.nodes.map(node=>({...node,x:100+((node.id-1)%4)*90,y:100+Math.floor((node.id-1)/4)*90,color:null})),
      edges:otherGraph.edges.map(edge=>({...edge,color:null,curve:0})),
      directed,nextId:count+1,nextEid:edges.length+1
    });
  }
  closeModal();
  return runPythonAlgorithm('isomorphism', {otherGraph});
}

/* ---------- player ---------- */
function stepFxPhase(){
  if(!stepFx)return 0;
  return clamp((performance.now()-stepFx.started)/800,0,1);
}
function stepFxProgress(){
  return Math.sin(Math.PI*stepFxPhase());
}
function animateStepFx(){
  if(stepFx&&stepFx.frame)cancelAnimationFrame(stepFx.frame);
  if(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches){stepFx=null;const stepText=$('#stepText');if(stepText)stepText.classList.remove('step-pop');return;}
  const stepText=$('#stepText');
  if(stepText){stepText.classList.remove('step-pop');void stepText.offsetWidth;stepText.classList.add('step-pop');}
  const animation={started:performance.now(),frame:0};stepFx=animation;
  const frame=now=>{
    if(stepFx!==animation)return;
    if(now-animation.started>=800){stepFx=null;draw();return;}
    draw();animation.frame=requestAnimationFrame(frame);
  };
  animation.frame=requestAnimationFrame(frame);
}
function cancelStepFx(){
  if(stepFx&&stepFx.frame)cancelAnimationFrame(stepFx.frame);
  stepFx=null;
  const stepText=$('#stepText');if(stepText)stepText.classList.remove('step-pop');
}
function setRun(r){
  stop(); run = r; stepIdx = 0; animateStepFx(); updatePlayer(); draw();
  toast(`พร้อมแล้ว ${r.steps.length} ขั้น — กด ▶ เพื่อเล่น หรือ ▶| ทีละขั้น`);
}
function resetPlanarityAnimation(restore=false){
  if(!planarityAnimation)return;
  if(planarityAnimation.frame)cancelAnimationFrame(planarityAnimation.frame);
  if(restore){
    const targets=planarityAnimation.targets;
    G.nodes.forEach(node=>{const point=targets.get(String(node.id));if(point){node.x=point.x;node.y=point.y;}});
    save();
  }
  planarityAnimation=null;
}
function preparePlanarityAnimation(layout){
  resetPlanarityAnimation();
  const points=G.nodes.map(node=>({id:String(node.id),point:layout[String(node.id)]})).filter(item=>Array.isArray(item.point)&&item.point.length===2);
  if(!points.length)return;
  const xs=points.map(item=>item.point[0]),ys=points.map(item=>item.point[1]);
  const minX=Math.min(...xs),maxX=Math.max(...xs),minY=Math.min(...ys),maxY=Math.max(...ys);
  const worldWidth=W/view.s,worldHeight=H/view.s,padding=64;
  const scale=Math.min((worldWidth-2*padding)/Math.max(1,maxX-minX),(worldHeight-2*padding)/Math.max(1,maxY-minY));
  const centerX=(W/2-view.x)/view.s,centerY=(H/2-view.y)/view.s;
  const layoutCenterX=(minX+maxX)/2,layoutCenterY=(minY+maxY)/2;
  planarityAnimation={frame:0,initial:new Map(),targets:new Map()};
  G.nodes.forEach(node=>planarityAnimation.initial.set(String(node.id),{x:node.x,y:node.y}));
  for(const item of points){
    planarityAnimation.targets.set(item.id,{
      x:centerX+(item.point[0]-layoutCenterX)*scale,
      y:centerY+(item.point[1]-layoutCenterY)*scale
    });
  }
}
function planarityAnimationSteps(){
  return [
    {msg:'เริ่มต้น: แสดงกราฟในตำแหน่งปัจจุบัน'},
    ...[25,50,75,100].map(percent=>({msg:`จัดตำแหน่งตาม planar embedding — ${percent}%`}))
  ];
}
function animatePlanarityTo(index){
  if(!planarityAnimation||!run||run.key!=='planarity')return;
  if(planarityAnimation.frame)cancelAnimationFrame(planarityAnimation.frame);
  const fraction=clamp(index/Math.max(1,run.steps.length-1),0,1),starts=new Map(),destinations=new Map();
  G.nodes.forEach(node=>{
    const id=String(node.id),initial=planarityAnimation.initial.get(id),target=planarityAnimation.targets.get(id);
    if(initial&&target){
      starts.set(id,{x:node.x,y:node.y});
      destinations.set(id,{x:initial.x+(target.x-initial.x)*fraction,y:initial.y+(target.y-initial.y)*fraction});
    }
  });
  const startTime=performance.now(),duration=500;
  const frame=now=>{
    if(!planarityAnimation)return;
    const progress=clamp((now-startTime)/duration,0,1),eased=1-Math.pow(1-progress,3);
    G.nodes.forEach(node=>{
      const from=starts.get(String(node.id)),to=destinations.get(String(node.id));
      if(from&&to){node.x=from.x+(to.x-from.x)*eased;node.y=from.y+(to.y-from.y)*eased;}
    });
    draw();
    if(progress<1)planarityAnimation.frame=requestAnimationFrame(frame);
    else{planarityAnimation.frame=0;if(fraction===1)save();}
  };
  planarityAnimation.frame=requestAnimationFrame(frame);
}
function clearRun(){ stop(); cancelStepFx(); resetPlanarityAnimation(true); run = null; stepIdx = 0; updatePlayer(); }
function go(i){ if(!run) return; stepIdx = clamp(i, 0, run.steps.length-1); if(run.key==='isomorphism') animateIsomorphismTo(stepIdx); if(run.key==='planarity') animatePlanarityTo(stepIdx); animateStepFx(); updatePlayer(); draw(); }
function stop(){ playing = false; clearTimeout(timer); const b = $('#bPlay'); if(b) b.textContent = '▶'; }
function play(){
  if(!run) return toast('กด "เริ่มรัน" ก่อน');
  if(playing) return stop();
  if(stepIdx >= run.steps.length-1) go(0);
  playing = true; $('#bPlay').textContent = '⏸'; tick();
}
function tick(){
  clearTimeout(timer);
  timer = setTimeout(() => {
    if(!playing || !run) return;
    if(stepIdx < run.steps.length-1){
      go(stepIdx+1);
      if(stepIdx >= run.steps.length-1){ stop(); setTimeout(showSummary, 600); } else tick();
    } else stop();
  }, 1200/speed);
}
function manual(fn){ stop(); fn(); }
function updatePlayer(){
  const n = run ? run.steps.length : 0, sl = $('#slider');
  sl.max = Math.max(0, n-1); sl.value = stepIdx;
  $('#stepLbl').textContent = n ? `ขั้น ${stepIdx+1}/${n}` : 'ขั้น 0/0';
  $('#stepText').textContent = run ? run.steps[stepIdx].msg : defaultStepText();
  $('#sumBtn').classList.toggle('glow', !!run && stepIdx === n-1);
}
function defaultStepText(){
  const T = TABS[algo];
  if(algo === 'color') return '👉 กด "▶ เริ่มรัน" เพื่อระบายสีแบบ Welsh–Powell';
  return `👉 ${T.s ? 'เลือก ' + T.s.replace(/^\S+\s/, '') + (T.t ? ' และ ' + T.t.replace(/^\S+\s/, '') : '') + ' แล้ว' : ''}กด "▶ เริ่มรัน"`;
}
function showSummary(){
  if(algo === 'analyze') return showAnalysis();
  if(!run) return toast('กด "เริ่มรัน" ก่อน แล้วค่อยดูสรุปผล');
  openModal(run.title, run.summary());
}

/* ---------- tabs ---------- */
const TABS = {
  analyze:{icon:'🔍', name:'วิเคราะห์', desc:'ดูภาพรวมของกราฟ: |V|, |E|, Degree, Σdeg = 2|E|, Connected/Components, ตรวจน้ำหนักติดลบ, Adjacency & Weight Matrix', s:null, t:null, run:() => showAnalysis()},
  dijkstra:{icon:'🛣️', name:'Dijkstra', desc:'หาเส้นทางสั้นที่สุดจากต้นทางไปทุกจุด โดยใช้น้ำหนักเป็นระยะทางหรือค่าขนส่ง', app:'เส้นทางขนส่งที่สั้น/ถูกที่สุด', s:'🚩 ต้นทาง', t:'🏁 ปลายทาง', run:runDijkstra},
  bellmanford:{icon:'➖', name:'Bellman–Ford', desc:'หาเส้นทางสั้นที่สุดโดยรองรับน้ำหนักติดลบ และตรวจ Negative Cycle', s:'🚩 ต้นทาง', t:'🏁 ปลายทาง', run:() => runPythonAlgorithm('bellmanford')},
  prim:{icon:'🌳', name:'Prim (MST)', desc:'สร้าง Spanning Tree ที่น้ำหนักรวมน้อยที่สุด โดยเพิ่มเส้นที่ถูกที่สุดทีละเส้น', app:'วางถนน/ท่อ/สายไฟให้ต้นทุนรวมต่ำสุด', s:'🚩 จุดเริ่ม', t:null, run:runPrim},
  kruskal:{icon:'🌲', name:'Kruskal (MST)', desc:'เลือกเส้นน้ำหนักน้อยที่สุดทีละเส้น โดยข้ามเส้นที่จะทำให้เกิดวงจร และแสดง Spanning Forest เมื่อกราฟไม่เชื่อมต่อ', s:null, t:null, run:runKruskal},
  euler:{icon:'🔁', name:'Euler Path/Circuit', desc:'ตรวจเงื่อนไข degree และใช้ Hierholzer หาเส้นทางที่ผ่านทุกเส้นครั้งเดียว รองรับกราฟมีทิศและเส้นขนาน', s:null, t:null, run:runEuler},
  bipartite:{icon:'◐', name:'Bipartite Graph', desc:'ตรวจว่าสามารถแบ่งจุดยอดเป็นสองฝั่งโดยทุกเส้นเชื่อมข้ามฝั่งหรือไม่ พร้อมแสดง partition และระบายสีจุดยอด', s:null, t:null, run:runBipartite},
  isomorphism:{icon:'🔁', name:'Isomorphic Graphs', desc:'เปรียบเทียบกราฟปัจจุบันกับอีกกราฟ แล้วแสดง mapping ของจุดยอดเมื่อมีโครงสร้างเหมือนกัน (กราฟอย่างง่ายไม่เกิน 12 จุด)', s:null, t:null, run:showIsomorphismInput},
  hamiltonian:{icon:'🧭', name:'Hamiltonian Path / Cycle', desc:'ค้นหา Hamiltonian Path และ Hamiltonian Cycle ด้วย Backtracking (ไม่เกิน 15 จุด) พร้อมเงื่อนไข Dirac/Ore', s:null, t:null, run:runHamiltonian},
  planarity:{icon:'📐', name:'Planarity / Kuratowski', desc:'ตรวจเกณฑ์ Euler และค้นหา K₅ / K₃,₃ minors ด้วยการลบจุดและหดเส้น (exact สูงสุด 10 จุดยอด; อาจรายงานว่าสรุปไม่ได้เมื่อค้นหาเกินขีดจำกัด)', s:null, t:null, run:runPlanarity},
  vertexconnectivity:{icon:'🔗', name:'Vertex Connectivity κ(G)', desc:'คำนวณจำนวนจุดยอดน้อยที่สุดที่ต้องตัดให้กราฟไม่เชื่อมต่อ พร้อมระบุชื่อจุดที่ต้องตัด', s:null, t:null, run:runVertexConnectivity},
  edgeconnectivity:{icon:'✂️', name:'Edge Connectivity λ(G)', desc:'คำนวณจำนวนเส้นเชื่อมน้อยที่สุดที่ต้องตัดให้กราฟไม่เชื่อมต่อ พร้อมระบุเส้นที่ต้องตัด', s:null, t:null, run:runEdgeConnectivity},
  degreeSequence:{icon:'🧮', name:'Degree Sequence', desc:'ตรวจด้วย Havel–Hakimi / Erdős–Gallai และสร้างกราฟอย่างง่ายจากลำดับ Degree ที่เป็นไปได้', s:null, t:null, run:showDegreeSequenceInput},
  complement:{icon:'◐', name:'Complement', desc:'สร้างกราฟเติมเต็ม โดยเชื่อมคู่จุดยอดที่ยังไม่มีเส้นเชื่อม (กราฟไม่มีทิศทางและไม่มีเส้นซ้ำ/loop)', s:null, t:null, run:runComplement},
  edgeColor:{icon:'🎨', name:'Edge Coloring', desc:'ระบายสีเส้นแบบ Greedy โดยเส้นที่มีจุดร่วมต้องคนละสี; สีแบบอัตโนมัติเป็นค่าประมาณ', s:null, t:null, run:runEdgeColoring},
  color:{icon:'🎨', name:'Vertex Coloring χ(G)', desc:'ระบายสีจุดแบบ Welsh–Powell พร้อมคำนวณ Chromatic Number แบบ Exact เมื่อมีไม่เกิน 15 จุด; ใช้กับตารางสอบ/แข่งขัน', app:'จุดที่เชื่อมกันต้องใช้สี/ช่วงเวลาต่างกัน; กราฟเชิงระนาบใช้ไม่เกิน 4 สีตามทฤษฎีบทสี่สี', s:null, t:null, run:runColoring},
  flow:{icon:'🚰', name:'Max Flow', desc:'Edmonds–Karp: หา Augmenting Path ด้วย BFS ซ้ำจนไหลเพิ่มไม่ได้ ใช้น้ำหนักเป็นความจุ (Capacity) ควรใช้กราฟแบบมีทิศ', app:'ปริมาณสินค้า/การจราจรสูงสุด และจุดคอขวด', s:'🟢 Source', t:'🔴 Sink', run:runFlow}
};
const LEGENDS = {
  analyze:'',
  dijkstra:'<span class="lg"><i style="background:#d7263d"></i>จุดปัจจุบัน</span><span class="lg"><i style="background:#3a86ff"></i>จุดที่กำลัง Relax</span><span class="lg"><i class="ln" style="background:#ef7d57"></i>เส้นที่กำลังตรวจ</span><span class="lg"><i style="background:#2a9d8f"></i>ปิดแล้ว</span><span class="lg"><i class="ln" style="background:#38b764"></i>เส้นทางสั้นสุด</span><span class="lg">🟨 ตัวเลขเหนือจุด = ระยะ</span>',
  kruskal:'<span class="lg"><i class="ln" style="background:#38b764"></i>เส้นใน Spanning Tree/Forest</span><span class="lg"><i class="ln" style="background:#94b0c2"></i>ข้ามเพราะเกิดวงจร</span>',
  euler:'<span class="lg"><i class="ln" style="background:#38b764"></i>เส้นทาง Euler</span>',
  bipartite:'<span class="lg"><i style="background:#ef7d57"></i>ฝั่งที่ 1</span><span class="lg"><i style="background:#41a6f6"></i>ฝั่งที่ 2</span>',
  isomorphism:'',
  hamiltonian:'<span class="lg"><i class="ln" style="background:#38b764"></i>Path/Cycle ที่ผ่านทุกจุดหนึ่งครั้ง</span>',
  planarity:'<span class="lg">K₅ หรือ K₃,₃ minor → ไม่เป็นกราฟเชิงระนาบ</span><span class="lg">กราฟเชิงระนาบต้องใช้ไม่เกิน 4 สี</span>',
  vertexconnectivity:'<span class="lg"><i style="background:#ef7d57"></i>จุดยอดที่ต้องตัด</span>',
  edgeconnectivity:'<span class="lg"><i class="dash"></i>เส้นเชื่อมที่ต้องตัด</span>',
  degreeSequence:'',
  complement:'',
  edgeColor:'<span class="lg">สีของเส้น = กลุ่มเส้นที่ไม่มีจุดร่วมกัน</span>',
  prim:'<span class="lg"><i class="ln" style="background:#ef7d57"></i>เส้นตัวเลือก</span><span class="lg"><i class="ln" style="background:#38b764"></i>อยู่ในต้นไม้</span><span class="lg"><i style="background:#2a9d8f"></i>จุดในต้นไม้</span>',
  color:'<span class="lg"><i style="background:#fff;border-color:#b13e53;border-width:4px"></i>จุดที่กำลังพิจารณา</span><span class="lg"><i class="ln" style="background:#ef7d57"></i>เส้นขัดแย้ง</span><span class="lg">สีของจุด = กลุ่ม (ช่วงเวลา/ช่องเก็บ)</span>',
  flow:'<span class="lg">ตัวเลข f/c = flow/ความจุ</span><span class="lg"><i class="ln" style="background:#3b5dc9"></i>มี flow</span><span class="lg"><i class="ln" style="background:#5d275d"></i>เต็ม</span><span class="lg"><i class="dash"></i>คอขวด (Min Cut)</span><span class="lg"><i style="background:#8338ec"></i>ฝั่ง S</span>'
};
function setTab(key){
  algo = TABS[key] ? key : 'dijkstra'; const T = TABS[algo];
  setIsomorphismSplit(algo === 'isomorphism');
  if(algo !== 'isomorphism'){
    isoGraph=null;isoFirstGraph=null;isoMapping=null;isoColors=[];
    isoSelNode=null;isoEdgePreview=null;lastActiveSide='left';
    $('#isoMappingLegend').replaceChildren();
    $('#isoMappingLegend').classList.remove('visible');
    $('#isoRightStatus').textContent='เลือก Isomorphic Graphs แล้วเริ่มเปรียบเทียบเพื่อแสดงกราฟที่สอง';
  }else{
    $('#isoRightStatus').textContent=isoGraph
      ? `กราฟที่สองมี ${isoGraph.nodes.length} จุด • ${isoGraph.edges.length} เส้น — ใช้เครื่องมือด้านบนแก้ไขได้`
      : 'เลือกเครื่องมือเพิ่มจุด/เชื่อมเส้น แล้วสร้างกราฟที่สองทางฝั่งขวา';
  }
  clearRun();
  $$('#tabs .btn').forEach(b => b.classList.toggle('on', b.dataset.tab === algo));
  $('#tabs').hidden=true;
  $('#toggleTabs').textContent='▼';
  $('#toggleTabs').setAttribute('aria-expanded','false');
  renderMainNavigation();
  $('#algoDesc').innerHTML = `<b>${T.icon} ${T.name}</b> — ${T.desc}` + (T.app ? `<span class="app">💡 การประยุกต์: ${T.app}</span>` : '');
  $('#lblS').style.display = T.s ? '' : 'none'; $('#lblT').style.display = T.t ? '' : 'none';
  $('#selRow').style.display = (T.s || T.t) ? '' : 'none';
  if(T.s) $('#lblSText').textContent = T.s; if(T.t) $('#lblTText').textContent = T.t;
  $('#runBtn').textContent = algo === 'analyze' ? '🔍 เปิดผลวิเคราะห์' : `▶ เริ่มรัน ${T.name}`;
  $('#player').style.display = algo === 'analyze' ? 'none' : '';
  $('#legend').innerHTML = LEGENDS[algo];
  updatePlayer(); save(); draw();
}
function refreshSelects(){
  for(const [sel, key] of [[$('#selS'), 'source'], [$('#selT'), 'sink']]){
    sel.innerHTML = '<option value="">— เลือกจุด —</option>' + G.nodes.map(n => `<option value="${n.id}">${esc(n.label)}${n.label !== 'v'+n.id ? ' (v'+n.id+')' : ''}</option>`).join('');
    sel.value = G[key] == null ? '' : String(G[key]);
  }
}
function updateBadge(){
  const comps = G.nodes.length ? components().length : 0;
  $('#badge').textContent = `|V| ${G.nodes.length} · |E| ${G.edges.length} · ${G.directed ? 'มีทิศ →' : 'ไม่มีทิศ —'}`;
  const controlGraph=lastActiveSide==='right'&&isoSplitView&&isoGraph?isoGraph:G;
  $('#dirIc').textContent = controlGraph.directed ? '→' : '—';
  $('#dirTxt').textContent = controlGraph.directed ? 'มีทิศ' : 'ไม่มีทิศ';
  $('#quick').textContent = `|V| = ${G.nodes.length} • |E| = ${G.edges.length} • ` + (comps <= 1 ? 'Connected ✔' : `⚠ ไม่ Connected (${comps} ส่วน)`) + ` • Undo ได้ ${undoStack.length} ขั้น`;
}
const HINTS = {
  move:'✋ ลากจุดเพื่อย้าย • ลากพื้นที่ว่างเพื่อเลื่อนจอ • แตะ 2 ครั้งที่จุด/เส้นเพื่อแก้ไข • ล้อเมาส์/บีบ 2 นิ้ว = ซูม',
  node:'⬛ แตะพื้นที่ว่างเพื่อเพิ่มจุดยอด (ลากจุดเดิมเพื่อย้ายได้)',
  edge:'🔗 แตะจุดแรก แล้วแตะจุดที่สอง เพื่อสร้างเส้นและใส่น้ำหนัก',
  edit:'✏️ แตะจุดเพื่อตั้งชื่อ (เช่น คลังสินค้า) • แตะเส้นเพื่อเปลี่ยนน้ำหนัก',
  bend:'〰️ ลากที่เส้นเพื่อดัดให้โค้ง • แตะเส้นเพื่อทำให้ตรง',
  reverse:'↔️ เลือกกราฟมีทิศทาง แล้วแตะเส้นที่ต้องการกลับทิศ (ย้อนได้ด้วย Undo)',
  del:'🗑️ แตะจุดหรือเส้นที่ต้องการลบ (กด Undo ได้)',
  style:'🎨 แตะจุดเพื่อเปลี่ยนสีหรือเลือกรูปแบบ PNG • แตะเส้นเพื่อเลือกสีหรือรูปแบบ (ถนน/ท่อ/สายไฟ)'
};
function updateHint(){
  let h = HINTS[tool];
  const useRight=lastActiveSide==='right'&&isoSplitView;
  const currentGraph=useRight?isoGraph:G, selected=useRight?isoSelNode:selNode;
  if(tool === 'edge' && selected != null && currentGraph){
    const node=currentGraph.nodes.find(item=>item.id===selected);
    if(node)h=`🔗 เลือก "${node.label}" แล้ว → แตะจุดปลายทาง (แตะจุดเดิมเพื่อสร้าง self-loop, แตะที่ว่างเพื่อยกเลิก)`;
  }
  $('#hint').textContent = h;
  const toolNames = {move:'ย้าย/เลื่อน',node:'เพิ่มจุด',edge:'เชื่อมเส้น',edit:'แก้ชื่อ/น้ำหนัก',style:'สี/รูปแบบจุดและเส้น',bend:'ดัดเส้น',reverse:'กลับทิศเส้น',del:'ลบ'};
  $('#toolStatus').textContent = `โหมด: ${toolNames[tool] || tool} · ${(currentGraph||G).directed ? 'Directed' : 'Undirected'}${isoSplitView?` · แก้ไข: กราฟที่ ${useRight?'2':'1'}`:''} · Ctrl/⌘+Z Undo · 1–8 เปลี่ยนโหมด`;
}

/* ---------- presets ---------- */
function mk(directed, nodes, edges, opt){
  const g = emptyGraph(); g.directed = directed;
  nodes.forEach(([x,y,l], i) => g.nodes.push({id:i+1, x, y, label:l, color:null}));
  g.nextId = nodes.length+1;
  edges.forEach(([u,v,w,c]) => g.edges.push({id:g.nextEid++, u, v, w, curve:c||0}));
  return Object.assign(g, opt || {});
}
function setSurface(graph,surface){
  if(!graph || !Array.isArray(graph.edges)) return graph;
  graph.edges.forEach(edge => { edge.surface = 'plain'; });
  return graph;
}
const PRESETS = {
  transport:{name:'🚚 โครงข่ายขนส่ง', tab:'dijkstra', desc:'หาเส้นทางส่งสินค้าจากคลังไปลูกค้าที่สั้นที่สุด (หน่วย: กม.)', build:() => mk(false,
    [[80,250,'คลังสินค้า'],[250,110,'ศูนย์กระจาย A'],[250,390,'ศูนย์กระจาย B'],[420,250,'จุดพักรถ'],[590,110,'ร้านค้า 1'],[590,390,'ร้านค้า 2'],[760,250,'ลูกค้า']],
    [[1,2,7],[1,3,9],[2,3,10],[2,4,15],[3,4,11],[2,5,20],[4,5,6],[4,6,9],[3,6,21],[5,7,8],[6,7,5]], {source:1, sink:7})},
  city:{name:'🏙️ แผนที่เมือง/โครงสร้างพื้นฐาน', tab:'prim', desc:'วางสายไฟ/ท่อประปาให้ทุกสถานที่เชื่อมกันด้วยต้นทุนต่ำสุด (ล้านบาท)', build:() => mk(false,
    [[100,100,'โรงไฟฟ้า'],[340,60,'โรงพยาบาล'],[580,110,'โรงเรียน'],[200,280,'ตลาด'],[430,260,'ศาลากลาง'],[680,290,'หมู่บ้าน A'],[120,460,'หมู่บ้าน B'],[390,460,'นิคมอุตสาหกรรม'],[640,480,'สถานีรถไฟ']],
    [[1,2,4],[1,4,3],[2,4,5],[2,5,6],[2,3,8],[3,5,7],[3,6,4],[4,5,2],[4,7,6],[5,8,5],[5,6,9],[7,8,7],[8,9,3],[6,9,5],[5,9,8],[4,8,9]], {source:1})},
  exam:{name:'📝 ตารางสอบ/ช่องเก็บสินค้า', tab:'color', desc:'วิชาที่เชื่อมกัน = มีนักเรียนสอบซ้อน ต้องอยู่คนละช่วงเวลา (สี = ช่วงเวลาสอบ)', build:() => {
    const names = ['คณิตศาสตร์','ฟิสิกส์','เคมี','ชีววิทยา','ภาษาอังกฤษ','ภาษาไทย','สังคมศึกษา','คอมพิวเตอร์'];
    const nodes = names.map((l,i) => { const a = (-90+i*45)*Math.PI/180; return [Math.round(400+230*Math.cos(a)), Math.round(300+230*Math.sin(a)), l]; });
    return mk(false, nodes, [[1,2,1],[1,3,1],[1,8,1],[1,7,1],[2,3,1],[2,8,1],[2,4,1],[3,4,1],[4,5,1],[5,6,1],[5,8,1],[6,7,1],[3,8,1]],
      {colorNames:['จันทร์ 09:00','จันทร์ 13:00','อังคาร 09:00','อังคาร 13:00','พุธ 09:00','พุธ 13:00']});
  }},
  k33:{name:'🧩 ปัญหา Utility (K₃,₃)', tab:'planarity', desc:'บ้าน 3 หลังและสาธารณูปโภค 3 แห่ง: K₃,₃ เป็นกราฟไม่เชิงระนาบ จึงต่อครบโดยไม่ให้เส้นตัดกันบนระนาบไม่ได้', build:() => mk(false,
    [[170,130,'บ้าน 1'],[170,300,'บ้าน 2'],[170,470,'บ้าน 3'],[620,130,'น้ำ'],[620,300,'ไฟฟ้า'],[620,470,'ก๊าซ']],
    Array.from({length:9},(_,i)=>[Math.floor(i/3)+1,4+i%3,1]))},
  fourmap:{name:'🗺️ แผนที่จำลอง 4 เขต (K₄)', tab:'color', desc:'แผนที่กราฟระนาบตัวอย่าง 4 เขต ทุกเขตมีพรมแดนร่วมกันอย่างน้อยหนึ่งเขต', build:() => mk(false,
    [[400,90,'เขต A'],[190,380,'เขต B'],[610,380,'เขต C'],[400,275,'เขต D']],
    [[1,2,1],[2,3,1],[3,1,1],[1,4,1],[2,4,1],[3,4,1]])},
  petersen:{name:'🕸️ Petersen Graph', tab:'hamiltonian', desc:'กราฟ 3-regular ที่ไม่ใช่ Hamiltonian: ตัวอย่างหักล้างว่ากราฟ regular ทุกกราฟต้องมี Hamiltonian cycle', build:() => {
    const edges=[];
    for(let i=0;i<5;i++)edges.push([i+1,(i+1)%5+1,1],[i+6,(i+2)%5+6,1],[i+1,i+6,1]);
    const nodes=Array.from({length:10},(_,i)=>{const a=2*Math.PI*i/10-Math.PI/2;return [400+230*Math.cos(a),300+230*Math.sin(a),`v${i+1}`];});
    return mk(false,nodes,edges);
  }},
  koenigsberg:{name:'🌉 สะพานทั้ง 7 แห่งของเคอนิกส์แบร์ก', tab:'euler', desc:'กราฟประวัติศาสตร์ 4 พื้นที่ 7 สะพาน มีจุดยอดดีกรีคี่ 4 จุด จึงไม่มี Euler Path', build:() => mk(false,
    [[130,150,'ฝั่งเหนือ'],[130,450,'ฝั่งใต้'],[440,170,'เกาะ Kneiphof'],[440,430,'เกาะ Lomse']],
    [[1,3,1,-0.3],[1,3,1,0.3],[2,3,1,-0.3],[2,3,1,0.3],[1,4,1,0],[2,4,1,0],[3,4,1,0.12]])},
  pipe:{name:'🚰 โครงข่ายท่อ/ถนน', tab:'flow', desc:'ส่งสินค้าจากโรงงานไปตลาดกลางได้มากที่สุดกี่หน่วย/ชม. และคอขวดอยู่ที่ไหน', build:() => mk(true,
    [[80,260,'โรงงาน'],[280,110,'คลัง A'],[280,410,'คลัง B'],[520,110,'ศูนย์ C'],[520,410,'ศูนย์ D'],[720,260,'ตลาดกลาง']],
    [[1,2,16],[1,3,13],[3,2,4],[2,4,12],[4,3,9],[3,5,14],[5,4,7],[4,6,20],[5,6,4]], {source:1, sink:6})},
  roadNetwork:{name:'🛣️ ถนนระหว่างเมือง',tab:'dijkstra',desc:'ค้นหาเส้นทางที่สั้นที่สุดบนโครงข่ายถนน โดยไฮไลต์เส้นทางที่เลือก',build:()=>setSurface(PRESETS.transport.build(),'road')},
  roadMst:{name:'🚧 สร้างถนนเชื่อมเมือง',tab:'prim',desc:'หาโครงข่ายถนนต้นทุนต่ำสุดด้วย Prim หรือ Kruskal',build:()=>setSurface(PRESETS.city.build(),'road')},
  bellmanExample:{name:'➖ เส้นทางมีน้ำหนักติดลบ',tab:'bellmanford',desc:'สาธิต Bellman–Ford บนกราฟมีน้ำหนักติดลบและไม่มี negative cycle',build:()=>mk(true,
    [[100,260,'ต้นทาง'],[310,100,'B'],[330,420,'C'],[570,260,'ปลายทาง']],
    [[1,2,4],[1,3,5],[2,3,-2],[2,4,4],[3,4,3]],{source:1,sink:4})},
  eulerCycle:{name:'🔁 Euler Circuit ตัวอย่าง',tab:'euler',desc:'วงจรสี่เหลี่ยมที่ทุกจุดมี degree คู่ เดินผ่านทุกเส้นได้ครบหนึ่งครั้ง',build:()=>mk(false,
    [[170,160,'A'],[570,160,'B'],[570,430,'C'],[170,430,'D']],[[1,2,1],[2,3,1],[3,4,1],[4,1,1]])},
  bipartiteExample:{name:'◐ กราฟสองส่วน K₂,₃',tab:'bipartite',desc:'ตรวจแบ่งจุดเป็นสองฝั่งและไฮไลต์เส้นระหว่าง partition',build:()=>mk(false,
    [[180,170,'A'],[180,400,'B'],[570,100,'X'],[570,285,'Y'],[570,470,'Z']],
    [[1,3,1],[1,4,1],[1,5,1],[2,3,1],[2,4,1],[2,5,1]])},
  isomorphismExample:{name:'🔁 เส้นทางสำหรับ Isomorphism',tab:'isomorphism',desc:'เปรียบเทียบเส้นทาง 4 จุดกับกราฟเดิมที่เปลี่ยนชื่อและลำดับจุด',build:()=>mk(false,
    [[160,160,'A'],[360,160,'B'],[560,160,'C'],[760,160,'D']],[[1,2,1],[2,3,1],[3,4,1]])},
  connectivityExample:{name:'✂️ วงจรสำหรับ Connectivity',tab:'vertexconnectivity',desc:'ใช้วงจร 5 จุดสาธิต minimum vertex cut และ edge cut',build:()=>mk(false,
    [[400,90,'A'],[680,250,'B'],[570,500,'C'],[230,500,'D'],[120,250,'E']],
    [[1,2,1],[2,3,1],[3,4,1],[4,5,1],[5,1,1]])},
  degreeExample:{name:'🧮 Degree Sequence (3, 2, 2, 1)',tab:'degreeSequence',desc:'ตัวอย่างลำดับดีกรีที่สร้างกราฟได้ ใช้ตรวจด้วย Havel–Hakimi',build:()=>mk(false,
    [[400,100,'A'],[200,350,'B'],[600,350,'C'],[400,500,'D']],[[1,2,1],[1,3,1],[1,4,1],[2,3,1]])},
  complementExample:{name:'◐ เส้นทางสำหรับ Complement',tab:'complement',desc:'ดูกราฟเติมเต็มของเส้นทาง 4 จุด',build:()=>mk(false,
    [[160,300,'A'],[360,300,'B'],[560,300,'C'],[760,300,'D']],[[1,2,1],[2,3,1],[3,4,1]])},
  edgeColorExample:{name:'🎨 ระบายสีเส้นแบบดาว',tab:'edgeColor',desc:'ระบายสีเส้นที่มีจุดร่วมให้ต่างสีกันบนกราฟดาว',build:()=>mk(false,
    [[400,300,'ศูนย์กลาง'],[170,130,'A'],[650,130,'B'],[650,470,'C'],[170,470,'D']],
    [[1,2,1],[1,3,1],[1,4,1],[1,5,1]])}
};
const ALGORITHM_EXAMPLES={
  analyze:'transport',dijkstra:'roadNetwork',bellmanford:'bellmanExample',prim:'roadMst',kruskal:'roadMst',
  euler:'eulerCycle',bipartite:'bipartiteExample',isomorphism:'isomorphismExample',
  hamiltonian:'petersen',planarity:'k33',vertexconnectivity:'connectivityExample',
  edgeconnectivity:'connectivityExample',degreeSequence:'degreeExample',complement:'complementExample',
  edgeColor:'edgeColorExample',color:'exam',flow:'pipe'
};
function showGenerator(){
  openModal('🧩 ตัวสร้างกราฟ', `<p>สร้างกราฟใหม่ (กด Undo เพื่อกลับกราฟเดิม)</p>
    <div class="row"><label class="sel">ชนิดกราฟ<select id="genType">
      <option value="complete">กราฟสมบูรณ์ Kₙ</option><option value="cycle">วงจร Cₙ</option>
      <option value="path">เส้นทาง Pₙ</option><option value="star">ดาว Star</option>
      <option value="bipartite">สองส่วน Kₘ,ₙ</option><option value="grid">Grid</option>
      <option value="hypercube">Hypercube Qₙ</option><option value="random">สุ่ม G(n,p)</option>
      <option value="tree">ต้นไม้สุ่ม</option><option value="dag">DAG สุ่ม</option>
      <option value="petersen">Petersen</option></select></label></div>
    <div class="row"><label class="sel">จำนวนจุด n <input id="genN" type="number" min="1" max="60" value="8"></label>
      <label class="sel">m (Kₘ,ₙ) / แถว <input id="genM" type="number" min="1" max="60" value="4"></label></div>
    <div class="row"><label class="sel">ความน่าจะเป็น p (0–1) <input id="genP" type="number" min="0" max="1" step="0.05" value="0.3"></label></div>
    <button type="button" class="btn primary" id="buildGraph">สร้างกราฟ</button>
    <p class="note">กราฟสมบูรณ์จำกัด n ≤ 40 และจำนวนจุดสูงสุด 60 เพื่อให้แอปตอบสนองได้ดี</p>`);
}
function buildGeneratedGraph(){
  const type = $('#genType').value, n = Number($('#genN').value), m = Number($('#genM').value), p = Number($('#genP').value);
  if(type === 'petersen'){
    const es = [];
    for(let i=0;i<5;i++){ es.push([i+1,(i+1)%5+1,1],[i+6,(i+1)%5+6,1],[i+1,i+6,1]); }
    const ns=Array.from({length:10},(_,i)=>{const a=2*Math.PI*i/10-Math.PI/2;return [400+230*Math.cos(a),300+230*Math.sin(a),`v${i+1}`];});
    return mk(false, ns, es);
  }
  if(!Number.isInteger(n) || n < 1 || n > 60) throw new Error('จำนวนจุดต้องเป็นจำนวนเต็ม 1–60');
  if(!Number.isInteger(m) || m < 1 || m > 60) throw new Error('ค่า m ต้องเป็นจำนวนเต็ม 1–60');
  if(!Number.isFinite(p) || p < 0 || p > 1) throw new Error('p ต้องอยู่ระหว่าง 0 ถึง 1');
  if(type === 'complete' && n > 40) throw new Error('Kₙ จำกัด n ≤ 40 เพื่อไม่ให้มีเส้นมากเกินไป');
  if(type === 'hypercube' && n > 6) throw new Error('Qₙ จำกัด n ≤ 6 (สูงสุด 64 จุด)');
  const count = type === 'bipartite' ? n + m : type === 'hypercube' ? 2 ** n : n;
  if(count > 60) throw new Error('กราฟนี้มีจุดเกินขีดจำกัด 60 จุด');
  const nodes = Array.from({length:count},(_,i)=>{
    const a = 2*Math.PI*i/count - Math.PI/2, r = Math.min(260, 48*count);
    return [400+r*Math.cos(a), 300+r*Math.sin(a), `v${i+1}`];
  });
  const edges = [];
  const add = (u,v) => edges.push([u+1,v+1,1]);
  if(type === 'complete'){
    for(let i=0;i<n;i++) for(let j=i+1;j<n;j++) add(i,j);
  } else if(type === 'cycle'){
    if(n < 3) throw new Error('วงจร Cₙ ต้องมี n ≥ 3');
    for(let i=0;i<n;i++) add(i,(i+1)%n);
  } else if(type === 'path'){
    for(let i=0;i<n-1;i++) add(i,i+1);
  } else if(type === 'star'){
    for(let i=1;i<n;i++) add(0,i);
  } else if(type === 'bipartite'){
    for(let i=0;i<n;i++) for(let j=0;j<m;j++) add(i,n+j);
  } else if(type === 'grid'){
    const rows = Math.max(1, Math.floor(Math.sqrt(n))), cols = Math.ceil(n/rows);
    for(let i=0;i<n;i++){ if(i%cols && i-1>=0) add(i-1,i); if(i-cols>=0) add(i-cols,i); }
    nodes.forEach((v,i)=>{ v[0]=100+(i%cols)*100; v[1]=100+Math.floor(i/cols)*100; });
  } else if(type === 'hypercube'){
    for(let i=0;i<count;i++) for(let b=0;b<n;b++){ const j=i^(1<<b); if(i<j) add(i,j); }
    nodes.forEach((v,i)=>{ v[2]=i.toString(2).padStart(n,'0'); });
  } else if(type === 'tree'){
    for(let i=1;i<n;i++) add(i,Math.floor(Math.random()*i));
  } else if(type === 'random' || type === 'dag'){
    for(let i=0;i<n;i++) for(let j=i+1;j<n;j++) if(Math.random()<p) add(i,j);
  }
  if(edges.length > 1500) throw new Error('กราฟมีเส้นเกิน 1,500 เส้น');
  return mk(type === 'dag', nodes, edges);
}
function showLayouts(){
  const items = [['circular','วงกลม'],['grid','ตาราง'],['force','Force-directed'],
    ['hierarchical','ลำดับชั้น'],['bipartite','สองคอลัมน์']];
  openModal('🪄 จัดวางอัตโนมัติ', '<p>จัดตำแหน่งจุดใหม่โดยไม่เปลี่ยนเส้นเชื่อม</p><div class="row">' +
    items.map(([key,label])=>`<button type="button" class="btn" data-layout="${key}">${label}</button>`).join('') + '</div>');
}
function applyLayout(kind){
  const nodes = G.nodes, n = nodes.length;
  if(!n) return toast('ยังไม่มีจุดยอด');
  const positions = new Map();
  if(kind === 'circular'){
    nodes.forEach((v,i)=>{ const a=2*Math.PI*i/n-Math.PI/2; positions.set(v.id,{x:400+Math.min(280,48*n)*Math.cos(a),y:300+Math.min(280,48*n)*Math.sin(a)}); });
  } else if(kind === 'grid'){
    const cols=Math.ceil(Math.sqrt(n));
    nodes.forEach((v,i)=>positions.set(v.id,{x:120+(i%cols)*100,y:100+Math.floor(i/cols)*100}));
  } else if(kind === 'bipartite'){
    const split=Math.ceil(n/2), left=nodes.slice(0,split), right=nodes.slice(split);
    left.forEach((v,i)=>positions.set(v.id,{x:180,y:100+i*500/Math.max(1,left.length-1)}));
    right.forEach((v,i)=>positions.set(v.id,{x:620,y:100+i*500/Math.max(1,right.length-1)}));
  } else if(kind === 'hierarchical'){
    const levels=new Map(nodes.map((v,i)=>[v.id,0]));
    for(let pass=0;pass<n;pass++) for(const e of G.edges) if(levels.has(e.u)&&levels.has(e.v))
      levels.set(e.v,Math.max(levels.get(e.v),levels.get(e.u)+1));
    const max=Math.max(0,...levels.values()), groups=new Map();
    nodes.forEach(v=>{const l=levels.get(v.id);if(!groups.has(l))groups.set(l,[]);groups.get(l).push(v);});
    for(const [l,group] of groups) group.forEach((v,i)=>positions.set(v.id,{x:100+(i+1)*600/(group.length+1),y:70+l*450/Math.max(1,max)}));
  } else {
    const pos=nodes.map(v=>({x:v.x,y:v.y}));
    for(let step=0;step<60;step++){
      const dx=Array(n).fill(0),dy=Array(n).fill(0);
      for(let i=0;i<n;i++) for(let j=i+1;j<n;j++){
        let x=pos[i].x-pos[j].x,y=pos[i].y-pos[j].y,d=Math.hypot(x,y)||1,f=1800/(d*d);
        dx[i]+=x/d*f;dy[i]+=y/d*f;dx[j]-=x/d*f;dy[j]-=y/d*f;
      }
      for(const e of G.edges){const i=nodes.findIndex(v=>v.id===e.u),j=nodes.findIndex(v=>v.id===e.v);if(i<0||j<0||i===j)continue;
        const x=pos[j].x-pos[i].x,y=pos[j].y-pos[i].y,d=Math.hypot(x,y)||1,f=d*d/500;
        dx[i]+=x/d*f;dy[i]+=y/d*f;dx[j]-=x/d*f;dy[j]-=y/d*f;
      }
      const temp=12*(1-step/60);
      pos.forEach((v,i)=>{v.x+=clamp(dx[i],-temp,temp);v.y+=clamp(dy[i],-temp,temp);});
    }
    nodes.forEach((v,i)=>positions.set(v.id,pos[i]));
  }
  commit(()=>nodes.forEach(v=>Object.assign(v,positions.get(v.id))),false);
  closeModal();fitView();toast('จัดวางกราฟแล้ว');
}
function searchNode(){
  const q=$('#nodeSearch').value.trim().toLocaleLowerCase();
  const n=G.nodes.find(v=>String(v.id)===q.replace(/^v/,'')||v.label.toLocaleLowerCase()===q);
  if(!n) return toast('ไม่พบจุดยอดที่ค้นหา');
  view.s=1.35;view.x=W/2-n.x*view.s;view.y=H/2-n.y*view.s;draw();toast(`พบ ${n.label}`);
}
function runQuickCommand(){
  const input=$('#quickCommand'), match=input.value.match(/^\s*(.+?)\s*-\s*(.+?)\s*:\s*(-?(?:\d+\.?\d*|\.\d+))\s*$/);
  if(!match) return toast('รูปแบบคำสั่งไม่ถูกต้อง ตัวอย่าง: v1-v2:5');
  const find=q=>G.nodes.find(v=>String(v.id)===q.replace(/^v/i,'')||v.label.toLocaleLowerCase()===q.toLocaleLowerCase());
  const u=find(match[1].trim()),v=find(match[2].trim()),w=Number(match[3]);
  if(!u||!v||!Number.isFinite(w)) return toast('ไม่พบจุดยอด หรือค่าน้ำหนักไม่ถูกต้อง');
  commit(()=>storeEdge(u.id,v.id,w));input.value='';toast(`เพิ่มเส้น ${u.label} ${G.directed?'→':'–'} ${v.label} = ${fmt(w)}`);
}
function showPresets(){
  openModal('📂 ตัวอย่าง',`<p>เลือกหมวดตัวอย่างที่ต้องการ</p><div class="example-categories">
    <button type="button" class="btn primary" data-example-category="algorithms">🧮 ตัวอย่างอัลกอริทึม</button>
    <button type="button" class="btn primary" data-example-category="problems">🧩 ตัวอย่างโจทย์</button>
  </div>`);
}
function renderExampleCategory(category){
  if(category==='algorithms'){
    const algorithms=Object.entries(ALGORITHM_EXAMPLES).map(([key,presetKey])=>{
    const preset=PRESETS[presetKey],tab=TABS[key];
    return `<div class="pcard"><b>${tab.icon} ${tab.name}</b><span style="font-size:14px">${preset.desc}<br><small>กดซ้ำเพื่อสุ่มรูปแบบและค่าน้ำหนักอีกครั้ง</small></span>
      <span style="font-size:13px">กราฟตัวอย่าง: <b>${preset.name}</b></span>
      <button type="button" class="btn primary" data-algorithm-example="${key}">เปิดตัวอย่างนี้</button></div>`;
    }).join('');
    return `<h3>ตัวอย่างอัลกอริทึม</h3><div class="pgrid">${algorithms}</div>`;
  }
  const presets=Object.entries(PRESETS).map(([key,preset])=>`
    <div class="pcard"><b>${preset.name}</b><span style="font-size:14px">${preset.desc}</span>
      <span style="font-size:13px">อัลกอริทึม: <b>${TABS[preset.tab].name}</b></span>
      <button type="button" class="btn primary" data-preset="${key}">เปิดตัวอย่างนี้</button></div>`).join('');
  return `<h3>ตัวอย่างโจทย์และกราฟ</h3><div class="pgrid">${presets}</div>`;
}
function showExampleCategory(category){
  const title=category==='algorithms'?'ตัวอย่างอัลกอริทึม':'ตัวอย่างโจทย์';
  $('#mtitle').textContent=`📂 ${title}`;
  $('#mbody').innerHTML=`<button type="button" class="btn mini" data-example-back>◀ กลับไปเลือกหมวด</button><p>เลือกตัวอย่างเพื่อแทนที่กราฟปัจจุบัน (กด Undo เพื่อกลับได้)</p>${renderExampleCategory(category)}`;
}
function loadPreset(k){
  const p = PRESETS[k]; if(!p) return;
  pushUndo(); G = p.build(); selNode = null; closeModal(); setTab(p.tab); afterChange(); fitView();
  toast(`โหลด "${p.name}" แล้ว → กด ▶ เริ่มรัน`);
}
function loadAlgorithmExample(key){
  const preset=PRESETS[ALGORITHM_EXAMPLES[key]],tab=TABS[key];
  if(!preset||!tab)return toast('ไม่พบตัวอย่างของอัลกอริทึมนี้');
  pushUndo();G=randomizeAlgorithmExample(key,preset.build());selNode=null;closeModal();setTab(key);afterChange();fitView();
  if(key==='analyze'){showAnalysis();return;}
  if(key==='degreeSequence'){showDegreeSequenceInput('3, 2, 2, 1');return;}
  if(key==='isomorphism'){
    const otherGraph={nodes:G.nodes.map((node,index)=>({id:index+1,label:`จุด ${String.fromCharCode(87+index)}`})),
      edges:[{id:1,u:1,v:3,w:1},{id:2,u:3,v:4,w:1},{id:3,u:4,v:2,w:1}],directed:false};
    runPythonAlgorithm('isomorphism',{otherGraph});return;
  }
  toast(`โหลดตัวอย่าง ${tab.name} แล้ว → กด ▶ เริ่มรัน`);
}
function randomizeAlgorithmExample(key,graph){
  const sample=sanitize(JSON.parse(JSON.stringify(graph)));
  const angle=Math.random()*Math.PI*2,radius=Math.min(250,45*sample.nodes.length);
  sample.nodes.forEach((node,index)=>{
    const theta=angle+2*Math.PI*index/Math.max(1,sample.nodes.length);
    const spread=0.82+Math.random()*0.36;
    node.x=400+radius*spread*Math.cos(theta);node.y=300+radius*spread*Math.sin(theta);
  });
  if(['dijkstra','prim','kruskal','flow'].includes(key)){
    sample.edges.forEach(edge=>{edge.w=1+Math.floor(Math.random()*15);});
  }
  return sample;
}
function algorithmPayload(algorithm, graph=G){
  return {
    algorithm,
    nodes:graph.nodes.map(({id,label})=>({id,label})),
    edges:graph.edges.map(({id,u,v,w})=>({id,u,v,w})),
    directed:graph.directed,
    source:graph.source ?? graph.nodes[0]?.id,
    sink:graph.sink ?? graph.nodes[graph.nodes.length-1]?.id,
    colorNames:graph.colorNames||[]
  };
}
async function requestAlgorithm(algorithm, graph=G){
  const response=await fetch('/api/run',{
    method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify(algorithmPayload(algorithm,graph))
  });
  const result=await response.json();
  if(!response.ok)throw new Error(result.error||`HTTP ${response.status}`);
  return result;
}
let activeQuiz=null;
async function showPractice(){
  const type=['mst','color','euler'][Math.floor(Math.random()*3)];
  let graph,algorithm,question,hint;
  if(type==='mst'){
    graph=mk(false,[[140,130,'A'],[380,80,'B'],[620,150,'C'],[500,390,'D'],[180,390,'E']],
      [[1,2,2],[2,3,5],[3,4,1],[4,5,4],[5,1,3],[1,3,7],[2,4,6]]);
    algorithm='kruskal';question='หา Minimum Spanning Tree: น้ำหนักรวมต่ำสุดเท่าไร?';hint='ลองเลือกเส้นจากน้ำหนักน้อยไปมาก และข้ามเส้นที่ทำให้เกิดวงจร';
  }else if(type==='color'){
    const chord=Math.random()<.5?[[1,3,1]]:[[1,3,1],[2,4,1]];
    graph=mk(false,[[400,80,'A'],[640,230,'B'],[550,480,'C'],[250,480,'D'],[160,230,'E']],
      [[1,2,1],[2,3,1],[3,4,1],[4,5,1],[5,1,1],...chord]);
    algorithm='color';question='ต้องใช้สีอย่างน้อยกี่สี เพื่อให้จุดที่เชื่อมกันมีสีต่างกัน?';hint='พิจารณาวงจรคี่: จุดรอบวงต้องใช้สีสลับกัน และจุดปิดวงอาจชนสีเดิม';
  }else{
    const hasCircuit=Math.random()<.5;
    graph=mk(false,[[180,150,'A'],[420,90,'B'],[650,230,'C'],[440,440,'D'],[180,390,'E']],
      [[1,2,1],[2,3,1],[3,4,1],[4,5,1],[5,1,1],...(hasCircuit?[]:[[1,3,1]])]);
    algorithm='euler';question='กราฟนี้มี Euler Circuit หรือไม่?';hint='กราฟเชื่อมต่อกันเมื่อพิจารณาจุดที่มีเส้น และทุกจุดต้องมี degree คู่';
  }
  pushUndo();G=graph;selNode=null;setTab(type==='mst'?'kruskal':type==='color'?'color':'euler');afterChange();fitView();
  toast('สุ่มกราฟแบบฝึกหัดให้แล้ว');
  try{
    const result=await requestAlgorithm(algorithm,graph);
    let answer;
    if(type==='mst')answer=result.total;
    else if(type==='color')answer=result.chromaticNumber;
    else answer=!!(result.exists&&result.isCircuit);
    if(answer==null)throw new Error('อัลกอริทึมไม่คืนคำตอบที่ต้องใช้ตรวจ');
    activeQuiz={kind:'practice',type,answer,hint,question};
    const choices=type==='euler'?[['true','มี'],['false','ไม่มี']]:
      [...new Set([answer,Math.max(1,answer-1),answer+1,answer+2])].sort((a,b)=>a-b).map(value=>[String(value),String(value)]);
    $('#practicePanel').innerHTML=`<b>🎯 แบบฝึกหัดสุ่ม</b><div class="hero">${esc(question)}</div><p>ดูกราฟแล้วแตะคำตอบ:</p><div class="row">${choices.map(([value,label])=>`<button type="button" class="btn quiz-choice" data-quiz-answer="${value}">${label}${type==='euler'?' Euler Circuit':''}</button>`).join('')}</div><button type="button" class="btn mini" data-quiz-hint>💡 ขอคำใบ้</button><div id="quizFeedback" aria-live="polite"></div>`;
    $('#practicePanel').classList.add('open');
  }catch(error){console.error('Practice question failed:',error);toast(`สร้างโจทย์ไม่ได้: ${error.message}`);}
}
function showLearning(section='practice'){
  openModal('📚 การเรียนรู้',`<nav class="learning-tabs" aria-label="เนื้อหาการเรียนรู้">
    <button type="button" class="btn" data-learning-tab="practice">🎯 แบบฝึกหัด</button>
    <button type="button" class="btn" data-learning-tab="lessons">📚 บทเรียน</button>
    <button type="button" class="btn" data-learning-tab="glossary">📖 อภิธานศัพท์</button>
  </nav><div id="learningContent"></div>`);
  renderLearningSection(section);
}
function renderLearningSection(section){
  $$('#mbody [data-learning-tab]').forEach(button=>button.classList.toggle('on',button.dataset.learningTab===section));
  const content=$('#learningContent');
  if(!content)return;
  if(section==='practice'){
    content.innerHTML=`<div class="hero">ฝึกคิดจากโจทย์กราฟแบบสุ่ม พร้อมตรวจคำตอบและรับคำใบ้</div><button type="button" class="btn primary" data-learning-start-practice>🎲 สุ่มโจทย์ใหม่</button>`;
  }else if(section==='lessons'){
    content.innerHTML=renderClassicsHTML();
  }else{
    content.innerHTML=renderGlossaryHTML();
  }
}
function markChoice(button,correct){
  button.classList.remove('answer-wrong','answer-correct');
  button.classList.add(correct?'answer-correct':'answer-wrong');
  button.setAttribute('aria-label',`${button.textContent.replace(/[✓✗]/g,'').trim()} ${correct?'ถูกต้อง':'ไม่ถูกต้อง'}`);
  button.dataset.answered=correct?'correct':'wrong';
  if(!button.querySelector('.answer-mark'))button.insertAdjacentHTML('beforeend',` <span class="answer-mark" aria-hidden="true">${correct?'✓':'✗'}</span>`);
  else button.querySelector('.answer-mark').textContent=correct?'✓':'✗';
}
function answerPractice(value){
  if(!activeQuiz)return;
  const correct=activeQuiz.type==='euler'?value===String(activeQuiz.answer):Number(value)===Number(activeQuiz.answer);
  const selected=$(`[data-quiz-answer="${CSS.escape(value)}"]`);
  if(selected)markChoice(selected,correct);
  const feedback=$('#quizFeedback');
  feedback.innerHTML=correct
    ?'<div class="hero">✔ ถูกต้อง! อธิบายเหตุผลของคำตอบได้ดีมาก</div><p>กด “เริ่มรัน” บนแผงอัลกอริทึมเพื่อดูวิธีทำทีละขั้น</p>'
    :'<div class="hero warn">ยังไม่ถูก ลองคิดจากโครงสร้างกราฟอีกครั้ง หรือขอคำใบ้</div>';
}
function renderClassicsHTML(){
  const cards=[
    ['koenigsberg','สะพานเคอนิกส์แบร์ก','4 พื้นที่ 7 สะพาน; degree เป็น 3,3,5,3 จึงมีจุดคี่ 4 จุดและไม่มี Euler Trail'],
    ['k33','Utility Problem: K₃,₃','บ้าน 3 หลังเชื่อมกับสาธารณูปโภค 3 แห่งครบทุกคู่; non-planar'],
    ['fourmap','ทฤษฎีบทสี่สี','เปิดแผนที่จำลอง K₄ (กราฟระนาบ 4 เขต) แล้วทดลองระบายสี'],
    ['petersen','Petersen Graph','กราฟ 3-regular แต่ไม่มี Hamiltonian cycle; หักล้างข้อความว่า regular ทุกกราฟมีวงจร Hamiltonian']
  ];
  const lessons=[
    ['handshake','Handshaking Lemma','Σ deg(v) = 2|E| เพราะทุกเส้นมีปลายสองด้าน; ดังนั้นจำนวนจุด degree คี่ต้องเป็นจำนวนคู่'],
    ['knight','Knight’s Tour','การเดินม้าครบทุกช่องหนึ่งครั้งคือ Hamiltonian path บนกราฟกระดานหมากรุก; ถ้ากลับจุดเริ่มได้คือ Hamiltonian cycle'],
    ['ramsey','Party Problem: R(3,3)=6','ในกลุ่ม 6 คน เลือกคนหนึ่ง แล้วจากอีก 5 คนมีอย่างน้อย 3 คนที่สัมพันธ์กับเขาแบบเดียวกัน. ในสามคนนั้น หากมีคู่ที่สัมพันธ์แบบเดียวกันจะได้สามเหลี่ยมสีเดียวกับคนแรก; มิฉะนั้นสามคนนั้นเป็นสามเหลี่ยมสีตรงข้าม'],
  ];
  return `<p>แตะบทเรียนเพื่ออ่านคำอธิบาย หรือโหลดกราฟคลาสสิกเพื่อทดลองอัลกอริทึม</p><h3>ตัวอย่างปัญหาคลาสสิก</h3>${cards.map(([id,title,desc])=>`<article class="classic-card"><b>${title}</b><p>${desc}</p><button type="button" class="btn mini primary" data-classic="${id}">โหลดกราฟและอัลกอริทึม</button>${id==='koenigsberg'?'<button type="button" class="btn mini" data-lesson="koenigsberg">อ่านประวัติและเหตุผล</button>':''}</article>`).join('')}<h3>แนวคิดสำคัญ</h3>${lessons.map(([id,title,desc])=>`<article class="classic-card"><button type="button" class="btn mini term-button" data-lesson="${id}">${title}</button><span>${desc}</span>${id==='knight'?'<p><button type="button" class="btn mini" data-open-knight>เปิดกระดาน Knight’s Tour 8×8</button></p>':''}</article>`).join('')}<div id="lessonDefinition" class="note" aria-live="polite">เลือกหัวข้อเพื่ออ่านคำอธิบายเพิ่มเติม</div><p class="note">แผนที่ตัวอย่างเป็นแบบจำลองกราฟ K₄ เพื่อสาธิตการระบายสี ไม่ใช่ข้อมูลภูมิศาสตร์หรือเขตแดนจริงของประเทศไทย</p>`;
}
function showClassics(){showLearning('lessons');}
let knightTour=[];
function renderKnightBoard(){
  const squares=Array.from({length:64},(_,index)=>{
    const step=knightTour.indexOf(index),color=(Math.floor(index/8)+index%8)%2?'dark':'light';
    return `<button type="button" class="btn knight-square ${color} ${step>=0?'visited':''}" data-knight-square="${index}" aria-label="แถว ${Math.floor(index/8)+1} คอลัมน์ ${index%8+1}">${step>=0?step+1:''}</button>`;
  }).join('');
  const closed=knightTour.length===64&&Math.abs(Math.floor(knightTour[0]/8)-Math.floor(knightTour[63]/8))===2&&Math.abs(knightTour[0]%8-knightTour[63]%8)===1||
    knightTour.length===64&&Math.abs(Math.floor(knightTour[0]/8)-Math.floor(knightTour[63]/8))===1&&Math.abs(knightTour[0]%8-knightTour[63]%8)===2;
  return `<p>แตะช่องเริ่มต้น แล้วแตะช่องถัดไปตามกติกาม้า (เดิน 2 ช่องทางหนึ่ง + 1 ช่องอีกทาง) ห้ามซ้ำช่อง</p><div class="knight-board">${squares}</div><p id="knightStatus">${knightTour.length===64?`ครบทุกช่อง! ${closed?'ปิดเป็น Knight’s Tour circuit ได้':'เป็น open Knight’s Tour'}`:`เดินแล้ว ${knightTour.length}/64 ช่อง`}</p><button type="button" class="btn mini" data-reset-knight>เริ่มใหม่</button>`;
}
function showKnightTour(){
  knightTour=[];openModal('♞ Knight’s Tour — ฝึกเดินม้า',renderKnightBoard());
}
const GLOSSARY={
  'Vertex / จุดยอด':'วัตถุหรือสถานที่ในกราฟ แทนด้วยจุดและมีรหัสกำกับ',
  'Edge / เส้นเชื่อม':'ความสัมพันธ์ระหว่างจุดยอดสองจุด; อาจมีทิศทางและน้ำหนัก',
  'Degree / ดีกรี':'จำนวนปลายเส้นที่ติดกับจุดยอด; self-loop นับสองครั้งในกราฟไม่มีทิศ',
  'Path / วิถี':'ลำดับจุดยอดที่ต่อกันด้วยเส้นเชื่อม',
  'Cycle / วงจร':'วิถีปิดที่กลับมาจุดเริ่มต้น',
  'Euler Circuit':'วงจรที่ผ่านทุกเส้นเชื่อมพอดีหนึ่งครั้ง',
  'Hamiltonian Cycle':'วงจรที่ผ่านทุกจุดยอดพอดีหนึ่งครั้ง',
  'Spanning Tree':'ต้นไม้ที่เชื่อมทุกจุดยอดของกราฟ ไม่มีวงจร',
  'MST':'Spanning Tree ที่ผลรวมน้ำหนักเส้นต่ำที่สุด',
  'Bipartite':'กราฟที่แบ่งจุดเป็นสองฝั่งได้ โดยทุกเส้นเชื่อมข้ามฝั่ง',
  'Planar':'กราฟที่วาดบนระนาบได้โดยเส้นไม่ตัดกัน (ยกเว้นที่จุดยอด)',
  'Chromatic Number':'จำนวนสีจุดยอดน้อยที่สุดที่ทำให้จุดที่ติดกันมีสีต่างกัน',
  'Flow / Capacity':'ปริมาณที่ไหลผ่านเส้น และขีดจำกัดสูงสุดของเส้นนั้น',
  'Negative Cycle':'วงจรที่ผลรวมน้ำหนักติดลบ ทำให้ไม่มีระยะทางสั้นที่สุดที่กำหนดได้'
};
function renderGlossaryHTML(){
  return `<p>แตะคำศัพท์เพื่อเปิดนิยาม</p><div class="glossary-list">${Object.entries(GLOSSARY).map(([term])=>`<button type="button" class="btn mini term-button" data-term="${esc(term)}">${esc(term)}</button>`).join('')}</div><div id="termDefinition" class="note" aria-live="polite">เลือกคำศัพท์ด้านบน</div><h3>บทพิสูจน์สั้น</h3><div class="classic-card"><b>Handshaking Lemma</b><p>นับคู่ “จุดยอด–ปลายเส้น” สองวิธี: รวมดีกรีทุกจุดได้จำนวนปลายทั้งหมด และแต่ละเส้นมีปลาย 2 ด้าน จึงได้ Σdeg(v)=2|E|</p></div><div class="classic-card"><b>Euler Circuit (กราฟไม่มีทิศทาง)</b><p>กราฟเชื่อมต่อที่จุดมี degree คู่ทุกจุดมี Euler Circuit: เดินตามเส้นที่ยังไม่ใช้จนกลับจุดเริ่ม แล้วนำวงจรย่อยที่เหลือมาแทรกจนใช้ครบทุกเส้น (Hierholzer)</p></div><div class="classic-card"><b>Max-Flow Min-Cut</b><p>ทุก flow มีค่าไม่เกิน capacity ของ cut ใด ๆ; เมื่อไม่มี augmenting path ใน residual graph, จุดที่ยังเข้าถึงได้จาก source กำหนด cut ที่ capacity เท่ากับ flow จึงเป็นค่าสูงสุดและ cut ต่ำสุด</p></div>`;
}
function showGlossary(){showLearning('glossary');}

/* ---------- export PNG ---------- */
function exportPNG(){
  if(!G.nodes.length) return toast('ยังไม่มีจุดยอดให้ส่งออก');
  let x0=Infinity, y0=Infinity, x1=-Infinity, y1=-Infinity;
  G.nodes.forEach(n => { x0=Math.min(x0,n.x); y0=Math.min(y0,n.y); x1=Math.max(x1,n.x); y1=Math.max(y1,n.y); });
  G.edges.forEach(e => { const g = edgeGeom(e); if(g){ x0=Math.min(x0,g.px); y0=Math.min(y0,g.py); x1=Math.max(x1,g.px); y1=Math.max(y1,g.py); } });
  x0 -= 100; x1 += 100; y0 -= 70; y1 += 70;
  const FOOT = 46, SC = 2, w = Math.ceil(x1-x0), h = Math.ceil(y1-y0)+FOOT;
  const oc = document.createElement('canvas'); oc.width = w*SC; oc.height = h*SC;
  const c = oc.getContext('2d'); c.scale(SC, SC);
  renderScene(c, w, h-FOOT, {x:-x0, y:-y0, s:1});
  c.fillStyle = INK; c.fillRect(0, h-FOOT, w, FOOT);
  c.fillStyle = '#ffcd75'; c.font = `bold 16px ${FONT}`; c.textAlign = 'left'; c.textBaseline = 'middle';
  c.fillText(`GRAPH THEORY LAB   |V| = ${G.nodes.length}   |E| = ${G.edges.length}   ${G.directed?'Directed':'Undirected'}${run ? '   • '+TABS[run.key].name : ''}`, 14, h-FOOT/2);
  const url = oc.toDataURL('image/png');
  openModal('🖼️ ส่งออก PNG', `<p>ขนาด ${w*SC} × ${h*SC} px (Scale 2) พร้อม |V| = ${G.nodes.length}, |E| = ${G.edges.length}</p>
    <a class="btn primary" download="graph-lab.png" href="${url}">⬇ ดาวน์โหลด PNG</a>
    <div class="note">📱 <b>iPhone/iPad หรือดาวน์โหลดไม่ได้:</b> กดค้างที่ภาพด้านล่าง แล้วเลือก "บันทึกลงในรูปภาพ" (Save to Photos)</div>
    <img src="${url}" class="preview" alt="graph">`);
  if(!IOS){ try{ const a = document.createElement('a'); a.href = url; a.download = 'graph-lab.png'; document.body.appendChild(a); a.click(); a.remove(); }catch(_){} }
}

/* ---------- help ---------- */
function showHelp(){
  openModal('❓ วิธีใช้ Graph Theory Lab', `<div class="hero">👋 ยินดีต้อนรับ! ทดลองอัลกอริทึมกราฟสำหรับงานขนส่งและผังเมือง</div>
  <h3>เริ่มใน 3 ขั้น</h3>
  <ol class="steps">
    <li><b>สร้างกราฟ</b> — กด ⬛ เพิ่มจุด แล้วแตะพื้นที่ว่าง → กด 🔗 เชื่อมเส้น แล้วแตะ 2 จุด (หรือกด 📂 ตัวอย่าง)</li>
    <li><b>เลือกอัลกอริทึม</b> ที่แผงด้านข้าง; กด ▼ เพื่อเปิดรายการเปลี่ยนอัลกอริทึม แล้วเลือกต้นทาง-ปลายทาง</li>
    <li><b>กด ▶ เริ่มรัน</b> แล้วดูทีละขั้นด้วย ⏮ ◀ ▶ ▶| ⏭ จากนั้นกด 📊 สรุปผล</li>
  </ol>
  <h3>เครื่องมือ</h3>
  <div class="tw"><table class="tbl">
    <tr><td>✋</td><td class="l">ลากจุด / เลื่อนจอ / แตะ 2 ครั้งเพื่อแก้ไข</td></tr>
    <tr><td>⬛</td><td class="l">เพิ่มจุดยอด</td></tr>
    <tr><td>🔗</td><td class="l">สร้างเส้น รวม self-loop, เส้นขนาน และน้ำหนักติดลบ</td></tr>
    <tr><td>✏️</td><td class="l">ตั้งชื่อจุด (เช่น คลังสินค้า) / แก้น้ำหนักเส้น</td></tr>
    <tr><td>〰️</td><td class="l">ดัดเส้นให้โค้ง / แตะเพื่อให้ตรง</td></tr>
    <tr><td>↔️</td><td class="l">กลับทิศเส้นในกราฟมีทิศทาง (Undo ได้)</td></tr>
    <tr><td>🗑️</td><td class="l">ลบจุดหรือเส้น</td></tr>
    <tr><td>⇄</td><td class="l">สลับกราฟมีทิศ / ไม่มีทิศ</td></tr>
    <tr><td>⌖</td><td class="l">จัดกราฟให้อยู่กึ่งกลางจอ</td></tr>
  </table></div>
  <div class="note">🔁 โหมด Isomorphic Graphs: ใช้เครื่องมือชุดเดียวกันสร้าง/แก้กราฟได้ทั้งฝั่งซ้ายและขวา (เลือกฝั่งด้วยการแตะหรือลากบนกราฟ) แล้วกดเริ่มรันและเลือก “ใช้กราฟที่วาดไว้ทางขวา” เพื่อเปรียบเทียบ</div>
  <h3>ทางลัด</h3>
  <p>Ctrl/⌘+Z = Undo • Ctrl/⌘+Y หรือ Ctrl/⌘+Shift+Z = Redo (ประมาณ 70 ขั้น) • 1–8 = เลือกเครื่องมือ • G = สร้างกราฟ • L = จัดวาง • F = จัดกึ่งกลาง • ← → = ย้อน/ถัดไป • Space = เล่น/หยุด • ล้อเมาส์หรือบีบ 2 นิ้ว = ซูม</p>
  <div class="note">🧩 สร้างกราฟ Kₙ, Cₙ, Pₙ, Star, Kₘ,ₙ, Grid, Qₙ, G(n,p), Random Tree, DAG และ Petersen • ตัวอย่างมี K₃,₃ และปัญหาสะพานทั้ง 7 ของเคอนิกส์แบร์ก • ค้นหาจุดยอดหรือพิมพ์คำสั่งเช่น v1-v2:-2</div>
  <div class="note">📚 ปุ่ม “ตัวอย่าง” แยกตัวอย่างอัลกอริทึมและตัวอย่างโจทย์ • ปุ่ม “การเรียนรู้” รวมแบบฝึกหัดสุ่ม บทเรียน และอภิธานศัพท์ • เลือกอัลกอริทึมจากแผงด้านข้าง; กด ▼ เพื่อเปลี่ยน • เลือก “สี / รูปแบบ” แล้วแตะจุดเพื่อเปลี่ยนสีหรือเลือกรูป PNG/SVG โปร่งใส และแตะเส้นเพื่อเปลี่ยนสีหรือรูปแบบเส้น • ตั้งค่าสี/ภาพพื้นหลัง ภาพเริ่มต้นของจุดใหม่ และซ่อนป้ายชื่อจุดหรือน้ำหนักเส้นได้จาก “ตั้งค่าพื้นหลัง / จุดยอด”</div>
  <div class="note">💾 ระบบบันทึกอัตโนมัติในเบราว์เซอร์ (localStorage): จุด เส้น น้ำหนัก ทิศทาง ชื่อ สี/รูป PNG และ Source/Sink; ภาพ PNG ต้นฉบับเก็บใน vertex และแอปใช้ไฟล์ย่อสำหรับแสดงผล • ถ้ามี SVG จะใช้เป็น vector โดยตรง</div>
  <p><button type="button" class="btn primary" id="helpPreset">📂 เปิดตัวอย่างสาธิต</button></p>`);
}

/* ---------- bind UI ---------- */
function init(){
  loadPreferences();
  const sharedGraph=decodeSharedGraph();
  if(sharedGraph)G=sharedGraph;
  $('#tabs').innerHTML = Object.entries(TABS).map(([k,T]) => `<button type="button" class="btn tab" data-tab="${k}">${T.icon} ${T.name}</button>`).join('');
  renderMainNavigation();
  loadVertexOptions().catch(error=>{console.error('Could not initialize vertex image choices:',error);toast(`โหลดภาพจุดยอดไม่ได้: ${error.message}`);});
  $('#tabs').addEventListener('click', e => { const b = e.target.closest('[data-tab]'); if(b) setTab(b.dataset.tab); });
  $('#toggleTabs').addEventListener('click',()=>{
    const expanded=$('#tabs').hidden;
    $('#tabs').hidden=!expanded;
    $('#toggleTabs').textContent=expanded?'▲':'▼';
    $('#toggleTabs').setAttribute('aria-expanded',String(expanded));
  });
  $('#toolbar').addEventListener('click', e => {
    const b = e.target.closest('[data-tool]');
    if(!b)return;
    tool=b.dataset.tool;selNode=null;edgePreview=null;isoSelNode=null;isoEdgePreview=null;
    $$('[data-tool]').forEach(x => x.classList.toggle('on', x === b));
    updateCanvasCursor(); updateHint(); draw();
  });
  $('#aDir').onclick = () => {
    withLastCanvasSide(()=>commit(()=>{G.directed=!G.directed;}));
    updateBadge();updateHint();
    const directed=lastActiveSide==='right'&&isoSplitView&&isoGraph?isoGraph.directed:G.directed;
    toast(directed?'→ เปลี่ยนเป็นกราฟมีทิศทาง':'— เปลี่ยนเป็นกราฟไม่มีทิศทาง');
  };
  $('#aUndo').onclick = undo;
  $('#aRedo').onclick = redo;
  $('#aStraight').onclick = () => withLastCanvasSide(()=>{
    if(!G.edges.some(e=>e.curve))return toast('เส้นตรงอยู่แล้วทั้งหมด');
    commit(()=>G.edges.forEach(e=>e.curve=0),false);toast('📏 รีเซ็ตเป็นเส้นตรงแล้ว');
  });
  $('#aPreset').onclick = showPresets;
  $('#aLibrary').onclick = showGraphLibrary;
  $('#aSettings').onclick = showSettings;
  $('#aLearning').onclick = ()=>showLearning();
  $('#aGenerate').onclick = showGenerator;
  $('#aLayout').onclick = showLayouts;
  $('#searchNode').onclick = () => withLastCanvasSide(searchNode);
  $('#nodeSearch').addEventListener('keydown',e=>{if(e.key==='Enter')withLastCanvasSide(searchNode);});
  $('#runCommand').onclick = () => withLastCanvasSide(runQuickCommand);
  $('#quickCommand').addEventListener('keydown',e=>{if(e.key==='Enter')withLastCanvasSide(runQuickCommand);});
  $('#aPNG').onclick = exportPNG;
  $('#aExportSteps').onclick = showStepExport;
  $('#aClear').onclick = () => withLastCanvasSide(()=>{
    if(!G.nodes.length)return;
    if(confirm('ล้างกราฟทั้งหมด? (กด Undo กลับได้)')){
      const directed=G.directed;commit(()=>{G=emptyGraph();G.directed=directed;});
      selNode=null;edgePreview=null;
    }
  });
  $('#aHelp').onclick = showHelp;
  $('#zIn').onclick = () => withLastCanvasSide(()=>zoomAt(W/2,H/2,1.25));
  $('#zOut').onclick = () => withLastCanvasSide(()=>zoomAt(W/2,H/2,0.8));
  $('#zFit').onclick = fitView;
  $('#selS').onchange = e => { G.source = e.target.value === '' ? null : +e.target.value; clearRun(); save(); draw(); };
  $('#selT').onchange = e => { G.sink = e.target.value === '' ? null : +e.target.value; clearRun(); save(); draw(); };
  $('#runBtn').onclick = () => TABS[algo].run();
  $('#bFirst').onclick = () => manual(() => go(0));
  $('#bPrev').onclick = () => manual(() => go(stepIdx-1));
  $('#bPlay').onclick = play;
  $('#bNext').onclick = () => manual(() => go(stepIdx+1));
  $('#bLast').onclick = () => manual(() => go(run ? run.steps.length-1 : 0));
  $('#slider').oninput = e => manual(() => go(+e.target.value));
  $$('[data-sp]').forEach(b => b.onclick = () => { speed = +b.dataset.sp; $$('[data-sp]').forEach(x => x.classList.toggle('on', x === b)); if(playing) tick(); });
  $('#sumBtn').onclick = showSummary;
  $('#clearRunBtn').onclick = () => {
    if(G.nodes.some(n => n.color != null)){ pushUndo(); G.nodes.forEach(n => n.color = null); }
    clearRun(); afterChange(); toast('ล้างผลแล้ว');
  };
  $('#mclose').onclick = closeModal;
  $('#modal').addEventListener('click', e => { if(e.target.id === 'modal') closeModal(); });
  $('#practicePanel').addEventListener('click',e=>{
    const quiz=e.target.closest('[data-quiz-answer]');
    if(quiz)return answerPractice(quiz.dataset.quizAnswer);
    if(e.target.closest('[data-quiz-hint]')&&activeQuiz)$('#quizFeedback').innerHTML=`<div class="note"><b>คำใบ้:</b> ${esc(activeQuiz.hint)}</div>`;
  });
  $('#mbody').addEventListener('click', e => {
    const learningTab=e.target.closest('[data-learning-tab]');
    if(learningTab)return renderLearningSection(learningTab.dataset.learningTab);
    if(e.target.closest('[data-learning-start-practice]')){closeModal();return showPractice();}
    const exampleCategory=e.target.closest('[data-example-category]');
    if(exampleCategory)return showExampleCategory(exampleCategory.dataset.exampleCategory);
    if(e.target.closest('[data-example-back]'))return showPresets();
    const vertexChoice=e.target.closest('[data-vertex-choice]');
    if(vertexChoice){
      const nodeId=Number($('#mbody').dataset.vertexNode),side=$('#mbody').dataset.vertexSide||'left';
      const filename=vertexChoice.dataset.vertexChoice,name=vertexChoice.dataset.vertexName||'';
      withCanvasSide(side,()=>{
        const node=G.nodes.find(item=>item.id===nodeId);
        if(!node)return toast('ไม่พบจุดยอดที่เลือก');
        commit(()=>{
          if(filename){node.vertexImage=filename;node.label=name;}
          else{delete node.vertexImage;node.label=`v${node.id}`;}
        });
      });
      closeModal();toast(filename?`ใช้รูป ${name} และตั้งชื่อจุดแล้ว`:'นำรูปจุดยอดออกแล้ว');return;
    }
    const vertexColor=e.target.closest('[data-vertex-color]');
    if(vertexColor){
      const nodeId=Number($('#mbody').dataset.vertexNode),side=$('#mbody').dataset.vertexSide||'left';
      const color=Number(vertexColor.dataset.vertexColor);
      withCanvasSide(side,()=>{
        const node=G.nodes.find(item=>item.id===nodeId);
        if(!node)return toast('ไม่พบจุดยอดที่เลือก');
        commit(()=>{node.color=color<0?null:color;});
      });
      closeModal();toast(color<0?'ล้างสีจุดยอดแล้ว':`เปลี่ยนสีจุดยอดเป็นสี ${color+1} แล้ว`);return;
    }
    if(e.target.closest('#saveLibraryGraph'))return saveCurrentGraph($('#libraryName').value);
    if(e.target.closest('#shareCurrentGraph'))return shareCurrentGraph();
    const libraryLoad=e.target.closest('[data-library-load]');
    if(libraryLoad){
      const item=library.find(entry=>entry.id===libraryLoad.dataset.libraryLoad);if(!item)return toast('ไม่พบกราฟในคลัง');
      pushUndo();G=sanitize(JSON.parse(JSON.stringify(item.graph)));closeModal();setTab(algo);afterChange();fitView();toast(`โหลด "${item.name}" แล้ว`);return;
    }
    const libraryDelete=e.target.closest('[data-library-delete]');
    if(libraryDelete){library=library.filter(entry=>entry.id!==libraryDelete.dataset.libraryDelete);persistLibrary();showGraphLibrary();return;}
    const libraryShare=e.target.closest('[data-library-share]');
    if(libraryShare){
      const item=library.find(entry=>entry.id===libraryShare.dataset.libraryShare);if(!item)return toast('ไม่พบกราฟในคลัง');
      const previous=G;G=sanitize(JSON.parse(JSON.stringify(item.graph)));shareCurrentGraph();G=previous;return;
    }
    const libraryCompare=e.target.closest('[data-library-compare]');
    if(libraryCompare){
      const item=library.find(entry=>entry.id===libraryCompare.dataset.libraryCompare);if(!item)return toast('ไม่พบกราฟในคลัง');
      closeModal();setTab('isomorphism');isoFirstGraph=null;isoGraph=sanitize(JSON.parse(JSON.stringify(item.graph)));isoMapping=null;isoColors=[];fitView();
      const rect=$('#stage').getBoundingClientRect();isoView=fitGraphView(isoGraph,Math.max(1,rect.width-W),H);
      $('#isoRightStatus').textContent=`กราฟที่สอง: ${item.name} • ${isoGraph.nodes.length} จุด • ${isoGraph.edges.length} เส้น`;
      draw();return;
    }
    const exportSteps=e.target.closest('[data-export-steps]');if(exportSteps)return downloadSteps(exportSteps.dataset.exportSteps);
    const p = e.target.closest('[data-preset]'); if(p) return loadPreset(p.dataset.preset);
    const algorithmExample=e.target.closest('[data-algorithm-example]');
    if(algorithmExample)return loadAlgorithmExample(algorithmExample.dataset.algorithmExample);
    const classic=e.target.closest('[data-classic]');if(classic)return loadPreset(classic.dataset.classic);
    if(e.target.closest('[data-open-knight]'))return showKnightTour();
    if(e.target.closest('[data-reset-knight]')){knightTour=[];$('#mbody').innerHTML=renderKnightBoard();return;}
    const knightSquare=e.target.closest('[data-knight-square]');
    if(knightSquare){
      const square=Number(knightSquare.dataset.knightSquare);
      if(knightTour.includes(square))return toast('ช่องนี้เดินไปแล้ว');
      if(knightTour.length){
        const previous=knightTour[knightTour.length-1],dr=Math.abs(Math.floor(previous/8)-Math.floor(square/8)),dc=Math.abs(previous%8-square%8);
        if(!((dr===2&&dc===1)||(dr===1&&dc===2)))return toast('ม้าเดินได้เฉพาะรูปตัว L');
      }
      if(knightTour.length<64)knightTour.push(square);
      $('#mbody').innerHTML=renderKnightBoard();return;
    }
    const quizAnswer=e.target.closest('[data-quiz-answer]');
    if(quizAnswer)return answerPractice(quizAnswer.dataset.quizAnswer);
    if(e.target.closest('[data-quiz-hint]')){
      if(activeQuiz)$('#quizFeedback').innerHTML=`<div class="note"><b>คำใบ้:</b> ${esc(activeQuiz.hint)}</div>`;
      return;
    }
    const term=e.target.closest('[data-term]');
    if(term){$('#termDefinition').innerHTML=`<b>${esc(term.dataset.term)}</b>: ${esc(GLOSSARY[term.dataset.term])}`;return;}
    const lesson=e.target.closest('[data-lesson]');
    if(lesson){
      const lessonDetails={
        handshake:'นับปลายเส้นทุกเส้นได้ 2|E| และนับจากแต่ละจุดได้ Σdeg(v) จึงเท่ากัน ผลสำคัญคือจำนวนจุด degree คี่ต้องเป็นเลขคู่',
        knight:'แทนช่องกระดาน 8×8 เป็นจุดยอด และเชื่อมสองช่องเมื่อม้าเดินถึงกันในหนึ่งก้าว; Knight’s Tour คือ Hamiltonian path ของกราฟนี้',
        ramsey:'ในกลุ่ม 6 คน เลือกคนหนึ่ง แล้วจากอีก 5 คนมีอย่างน้อย 3 คนที่สัมพันธ์กับเขาแบบเดียวกัน. ในสามคนนั้น หากมีคู่ที่สัมพันธ์แบบเดียวกันจะได้สามเหลี่ยมสีเดียวกับคนแรก; มิฉะนั้นสามคนนั้นเป็นสามเหลี่ยมสีตรงข้าม',
        koenigsberg:'ปัญหาสะพานทั้ง 7 แห่งถูก Euler ศึกษาในปี 1736 โดยแทนพื้นที่เป็นจุดยอดและสะพานเป็นเส้นเชื่อม ดีกรีทั้งสี่คือ 3, 3, 5, 3 รวม 14 = 2×7 แต่มีจุด degree คี่ 4 จุด ขณะที่ Euler Path ต้องมีจุดคี่ 0 หรือ 2 จุด จึงเดินผ่านสะพานครบหนึ่งครั้งไม่ได้ งานชิ้นนี้เป็นจุดเริ่มต้นสำคัญของทฤษฎีกราฟ'
      };
      const lessonDefinition=$('#lessonDefinition');
      if(lessonDefinition)lessonDefinition.innerHTML=`<b>${esc(lesson.textContent)}</b><br>${esc(lessonDetails[lesson.dataset.lesson])}`;
      else openModal(lesson.textContent,`<div class="hero">${esc(lessonDetails[lesson.dataset.lesson])}</div>`);
      return;
    }
    if(e.target.closest('#buildDegreeSequence')) return runDegreeSequenceFromInput();
    if(e.target.closest('#runIsomorphismCompare')) return runIsomorphismComparison();
    if(e.target.closest('#buildGraph')){
      try{pushUndo();G=buildGeneratedGraph();selNode=null;clearRun();afterChange();closeModal();fitView();setTab('analyze');toast('สร้างกราฟสำเร็จ');}
      catch(error){toast(`สร้างกราฟไม่ได้: ${error.message}`);}
      return;
    }
    const layout=e.target.closest('[data-layout]');if(layout)return withLastCanvasSide(()=>applyLayout(layout.dataset.layout));
    if(e.target.closest('#helpPreset')) return showPresets();
    const edgeColor=e.target.closest('[data-edge-color]');
    if(edgeColor){
      const edgeId=Number($('#mbody').dataset.edgeId),side=$('#mbody').dataset.edgeSide||'left';
      const color=Number(edgeColor.dataset.edgeColor);
      withCanvasSide(side,()=>{
        const edge=G.edges.find(item=>item.id===edgeId);
        if(!edge)return toast('ไม่พบเส้นที่เลือก');
        commit(()=>{edge.color=color<0?null:color;},false);
      });
      closeModal();toast(color<0?'ล้างสีเส้นแล้ว':`เปลี่ยนสีเส้นเป็นสี ${color+1} แล้ว`);return;
    }
    const edgeSurface=e.target.closest('[data-edge-surface]');
    if(edgeSurface){
      const edgeId=Number($('#mbody').dataset.edgeId),side=$('#mbody').dataset.edgeSide||'left';
      withCanvasSide(side,()=>{
        const edge=G.edges.find(item=>item.id===edgeId);
        if(!edge)return toast('ไม่พบเส้นที่เลือก');
        commit(()=>{edge.surface=edgeSurface.dataset.edgeSurface;},false);
      });
      closeModal();toast(`เปลี่ยนรูปแบบเส้นเป็น ${EDGE_SURFACES[edgeSurface.dataset.edgeSurface]||'เส้นธรรมดา'}`);return;
    }
    const cn = e.target.closest('[data-cname]');
    if(cn){
      const i = +cn.dataset.cname;
      const s = prompt('ตั้งชื่อความหมายของสีนี้ (เช่น จันทร์ 09:00, ช่องเก็บ A):', cName(i));
      if(s !== null){ G.colorNames[i] = s.trim() || `สี ${i+1}`; save(); if(run && run.key === 'color') $('#mbody').innerHTML = run.summary(); }
    }
  });
  $('#mbody').addEventListener('keydown', e => {
    if(e.target.id === 'degreeSequenceInput' && e.key === 'Enter'){
      e.preventDefault();
      runDegreeSequenceFromInput();
    }
  });
  window.addEventListener('keydown', e => {
    const tg = e.target.tagName; if(tg === 'INPUT' || tg === 'SELECT' || tg === 'TEXTAREA') return;
    if((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'z'){ e.preventDefault(); if(e.shiftKey) redo(); else undo(); }
    else if((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'y'){ e.preventDefault(); redo(); }
    else if(e.key === 'Escape')closeModal();
    else if(e.key.toLowerCase() === 'g') showGenerator();
    else if(e.key.toLowerCase() === 'l') showLayouts();
    else if(e.key.toLowerCase() === 'f') fitView();
    else if(/^[1-8]$/.test(e.key)){
      const tools=['move','node','edge','edit','style','bend','reverse','del'], key=tools[Number(e.key)-1];
      const button=$(`[data-tool="${key}"]`);
      if(button){tool=key;selNode=null;edgePreview=null;$$('[data-tool]').forEach(x=>x.classList.toggle('on',x===button));updateCanvasCursor();updateHint();draw();}
    }
    else if(e.key === 'ArrowRight') manual(() => go(stepIdx+1));
    else if(e.key === 'ArrowLeft') manual(() => go(stepIdx-1));
    else if(e.key === ' '){ e.preventDefault(); play(); }
  });

  const savedTab = sharedGraph ? null : load();
  if(!sharedGraph&&!savedTab) G = PRESETS.transport.build();
  if('ResizeObserver' in window) new ResizeObserver(() => resize()).observe($('#stage'));
  else window.addEventListener('resize', resize);
  resize();
  setTab(savedTab || 'dijkstra');
  afterChange();
  if(!savedTab){ fitView(); if(sharedGraph)setTimeout(()=>toast('โหลดกราฟจาก URL แชร์แล้ว'),0);else setTimeout(showHelp,300); }
}
if(document.fonts && document.fonts.ready) document.fonts.ready.then(() => draw());
if('serviceWorker' in navigator && location.protocol !== 'file:'){
  navigator.serviceWorker.register('/service-worker.js').catch(error => console.error('PWA service worker registration failed:', error));
}
init();
})();
</script>
</body>
</html>
"""

PORT_START = int(os.environ.get("PORT", "8765"))


def lan_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        request_path = unquote(urlsplit(self.path).path)
        if request_path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
        vertex_dir = Path(__file__).with_name("vertex")
        if request_path == "/api/vertices":
            try:
                image_files = [*vertex_dir.glob("*.png"), *vertex_dir.glob("*.svg")]
                vertices = [
                    {
                        "name": image.stem,
                        "filename": image.name,
                        "url": (
                            f"/vertex/thumbs/{quote(image.name)}"
                            if image.suffix.lower() == ".png"
                            else f"/vertex/vector/{quote(image.name)}"
                        ),
                    }
                    for image in sorted(image_files, key=lambda item: item.name.casefold())
                ]
            except OSError as error:
                body = json.dumps({"error": f"อ่านรายการภาพจุดยอดไม่ได้: {error}"}, ensure_ascii=False).encode("utf-8")
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            body = json.dumps({"vertices": vertices}, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(body)
            return
        if request_path.startswith("/vertex/vector/"):
            filename = request_path.removeprefix("/vertex/vector/")
            vector_file = vertex_dir / filename
            if Path(filename).name != filename or Path(filename).suffix.lower() != ".svg":
                self.send_error(404)
                return
            try:
                body = vector_file.read_bytes()
            except OSError:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", "image/svg+xml; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Cache-Control", "public, max-age=86400")
            self.end_headers()
            self.wfile.write(body)
            return
        if request_path.startswith("/vertex/thumbs/"):
            filename = request_path.removeprefix("/vertex/thumbs/")
            thumbnail = vertex_dir / "thumbs" / filename
            source = vertex_dir / filename
            if Path(filename).name != filename or not filename.lower().endswith(".png") or not source.is_file():
                self.send_error(404)
                return
            try:
                body = thumbnail.read_bytes()
            except OSError:
                self.send_error(404, "ไม่พบภาพย่อ กรุณาสร้าง vertex/thumbs จากภาพต้นฉบับ")
                return
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "public, max-age=86400")
            self.end_headers()
            self.wfile.write(body)
            return
        assets = {
            "/head.png": (Path("img") / "head.png", "image/png"),
            "/mascot_clean.png": (Path("img") / "mascot_clean.png", "image/png"),
            "/web.png": (Path("img") / "web.png", "image/png"),
            "/service-worker.js": (Path("service-worker.js"), "text/javascript; charset=utf-8"),
            "/manifest.webmanifest": (Path("manifest.webmanifest"), "application/manifest+json; charset=utf-8"),
        }
        if request_path in assets:
            asset_path, content_type = assets[request_path]
            asset = Path(__file__).parent / asset_path
            try:
                body = asset.read_bytes()
            except OSError:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            cache_control = "no-cache" if asset_path.name == "service-worker.js" else "public, max-age=3600"
            self.send_header("Cache-Control", cache_control)
            self.end_headers()
            self.wfile.write(body)
            return
        body = HTML.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/api/run":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0 or length > 2_000_000:
            self.send_error(413, "ข้อมูลกราฟไม่ถูกต้องหรือมีขนาดใหญ่เกินไป")
            return
        try:
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise ValueError("ข้อมูลคำขอไม่ถูกต้อง")
            result = run_algorithm(payload)
        except (ValueError, UnicodeDecodeError) as error:
            body = json.dumps({"error": str(error)}, ensure_ascii=False).encode("utf-8")
            self.send_response(400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        body = json.dumps(result, ensure_ascii=False, allow_nan=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass  # ปิด log เพื่อให้ Terminal สะอาด


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    # สร้างไฟล์ HTML ไว้ข้าง ๆ เพื่อเปิดแบบออฟไลน์ได้
    out = Path(__file__).with_name("graph_lab.html")
    try:
        out.write_text(HTML, encoding="utf-8")
    except OSError:
        out = None

    httpd = None
    port = PORT_START
    ports = [PORT_START] if "PORT" in os.environ else range(PORT_START, PORT_START + 40)
    for p in ports:
        try:
            httpd = http.server.ThreadingHTTPServer(("0.0.0.0", p), Handler)
            port = p
            break
        except OSError:
            continue

    if httpd is None:
        print("เปิดเซิร์ฟเวอร์ไม่ได้ → เปิดไฟล์ HTML สำรอง (การรันอัลกอริทึมต้องใช้ Python server)")
        if out and "PORT" not in os.environ:
            webbrowser.open(out.as_uri())
        return

    url = f"http://localhost:{port}"
    print("=" * 56)
    print("  GRAPH THEORY LAB  (Logistics & Urban Planning)")
    print("=" * 56)
    if "PORT" in os.environ:
      print(f"  Web service listening on assigned port {port}")
    else:
      print(f"  คอมพิวเตอร์นี้ : {url}")
      print(f"  มือถือ/แท็บเล็ต : http://{lan_ip()}:{port}  (Wi-Fi เดียวกัน)")
      if out:
        print(f"  ไฟล์ออฟไลน์    : {out}")
      print("  กด Ctrl+C เพื่อปิดโปรแกรม")
    print("=" * 56)

    if "PORT" not in os.environ:
      threading.Timer(0.7, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nปิดเซิร์ฟเวอร์แล้ว")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
