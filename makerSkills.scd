s.boot;
OSCdef.freeAll;
~path = PathName(thisProcess.nowExecutingPath).parentPath;
~buffers = Array.new;
PathName(~path ++ "Audio/").entries.collect{ |file|
		~buffers = ~buffers.add(Buffer.readChannel(s, file.fullPath, channels:0).normalize(0.8, false))};
(
SynthDef(\grain,
{
	arg rate=1, modFreq=0, modAmp=5, buf=0, amp=1;
	var sig;
	sig = GrainBuf.ar(
		1, //numChannels
		Dust.ar(20!2), //trigger
		LFNoise1.kr(0.15).exprange(2,5), //bufLen

		buf, //soundfile
		rate,
		Phasor.ar(0, BufRateScale.kr(buf), 0, BufFrames.ir(buf)), //pos
		mul:0.4);
		sig = sig * LFPar.kr(modFreq, mul: modAmp);
		sig = sig * 0.04;
		sig = sig * amp;
		Out.ar(0,sig);
}
).add;
)
~def = Synth(\grain, [\buf, ~buffers[0], \modFreq, 0])
(
OSCdef(\rateOSC, {
	arg msg, time, addr, port;
	~def.set(\rate, msg[1].asFloat);
	msg[1].postln;
}, '/rate', recvPort:5005);

OSCdef(\amOSC, {
	arg msg, time, addr, port;
	~def.set(\modFreq, msg[1].asFloat);
	msg[1].postln;
}, '/AM', recvPort:5005);

OSCdef(\bufOSC, {
	arg msg, time, addr, port;
	~def.set(\buf, ~buffers[msg[1].asFloat]);
	msg[1].postln;
}, '/buf', recvPort:5005)
)
