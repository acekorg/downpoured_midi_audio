import midirender_runtimidity
import midirender_util
import sys
import time

sys.path.append('..')
from bmidilib import bmidiplay, bmiditools

tmpfilename = 'tmpout.mid'

class BMidiRenderPlayback():
	playingState = 'stopped' #or 'paused' or 'playing'.
	midiPlayerObject = None
	def __init__(self, fnToggleBtn, fnGetSlider, fnSetSlider):
		self.fnToggleBtn = fnToggleBtn
		self.fnGetSlider = fnGetSlider
		self.fnSetSlider = fnSetSlider
		
		#right now, we create a new instance of a MciMidiPlayer or TimidityMidiPlayer every time Play is pressed.
		#this might not be the best way to go...
		
		self.fnSetSlider(0)
		self.currentTime = 0
		self.lengthTime = 0
		self.fnToggleBtn('stop')
	
	def load(self,newLength):
		self.currentTime = 0
		self.lengthTime = newLength
		self.fnSetSlider(0)
		self.fnToggleBtn('stop')
		
	def isPlaying(self):
		return self.playingState=='playing'
	
	def playSliderThread(self):
		while self.playingState=='playing':
			if not self.midiPlayerObject.isPlaying:
				if isinstance(self.midiPlayerObject,bmidiplay.MciMidiPlayer) or self.currentTime>=self.lengthTime-3:
					self.actionStop() #as if Stop had been clicked. will exit this loop.
				else:
					self.actionPause()
				break
			else:
				if self.currentTime>=self.lengthTime:
					self.fnSetSlider(self.currentTime)
					self.currentTime+=0.0 #just wait here, until it stops playing.
				else:
					self.fnSetSlider(self.currentTime)
					self.currentTime+=0.2
				
			time.sleep(0.2)
			
	
	def actionPlay(self, midiCopy, arParams, strConfig, bRenderPreview = False):
		if self.playingState == 'playing': return
		
		if self.midiPlayerObject != None and self.midiPlayerObject.isPlaying: return #evidently still playing something...
		
		#update the currentTime
		self.currentTime = self.fnGetSlider()
		
		if sys.platform=='win32' and not bRenderPreview:
			#play through default synth, mci
			self.midiPlayerObject = bmidiplay.MciMidiPlayer()
			self.midiPlayerObject.playMidiObject(midiCopy, False, fromMs=self.currentTime * 1000)
			
		else:
			#play with timidity. we'll have to cut the midi ourselves.
			bmiditools.makeVeryRoughTimeExcerpt(midiCopy, float( self.currentTime)/float(self.lengthTime))
			#~ print midiCopy
			midiCopy.open(tmpfilename,'wb')
			midiCopy.write()
			midiCopy.close()
			
			
			if bRenderPreview:
				self.midiPlayerObject = midirender_runtimidity.RenderTimidityMidiPlayer()
				self.midiPlayerObject.setConfiguration(strConfig)
				self.midiPlayerObject.setParameters(arParams)
				self.midiPlayerObject.playMidiObject(midiCopy, False)
			else:
				self.midiPlayerObject = bmidiplay.TimidityMidiPlayer()
				self.midiPlayerObject.playMidiObject(midiCopy, False)
			
			
		self.playingState = 'playing'
		self.fnToggleBtn('play')
		midirender_util.makeThread(self.playSliderThread)
		
		
		
	def actionPause(self):
		if self.playingState=='paused': return
		
		if self.playingState=='playing':
			self.midiPlayerObject.signalStop()
			#~ if not isinstance(self.midiPlayerObject,bmidiplay.MciMidiPlayer): time.sleep(0.5) #time for process to die
			
		self.playingState = 'paused' #stops the sliderThread
		self.fnToggleBtn('pause')
		
	def actionStop(self):
		if self.playingState=='stopped': return
		
		if self.playingState=='playing':
			self.midiPlayerObject.signalStop()
			#~ if not isinstance(self.midiPlayerObject,bmidiplay.MciMidiPlayer): time.sleep(0.5) #time for process to die
			
		self.playingState = 'stopped' #stops the sliderThread
		self.currentTime = 0.0
		self.fnSetSlider(0.0)
		
		self.fnToggleBtn('stop')
			
			
	