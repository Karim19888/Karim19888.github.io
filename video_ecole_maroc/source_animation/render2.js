const { chromium } = require('playwright');const {spawn}=require('child_process');
(async()=>{
  const [,,hash,out]=process.argv;const FPS=30,DUR=56.5;
  const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
  await p.goto('file://'+__dirname+'/build/video.html#'+hash);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(800);
  const ff=spawn('ffmpeg',['-v','error','-y','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-','-i','mix.wav',
    '-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',out],{stdio:['pipe','inherit','inherit']});
  for(let f=0;f<FPS*DUR;f++){await p.evaluate(t=>render(t),f/FPS);
    const buf=await p.screenshot({type:'jpeg',quality:93});
    if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));
    if(f%300===0)console.log(hash,f);}
  ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();})();
