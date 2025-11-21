import {Config} from '@remotion/cli/config';

// Studio port configuration (auto-select free port)
// Config.setStudioPort(8082);  // Commented out - let Remotion auto-select

Config.setVideoImageFormat('jpeg');
Config.setOverwriteOutput(true);
Config.setCodec('h264');
Config.setPixelFormat('yuv420p');

// GPU acceleration (user has GPU machine)
Config.setChromiumOpenGlRenderer('angle');
Config.setChromiumHeadlessMode(true);

// Output settings - unified with sushi pipeline
// All videos render to: ../sushi/videos/{video-id}/output/
Config.setOutputLocation('../sushi/videos');

export default Config;
