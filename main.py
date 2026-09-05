import json
import random
import os
from datetime import datetime, date, timedelta
import threading
import time
import math

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.carousel import Carousel
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Line, Ellipse, Rectangle, Triangle, PushMatrix, PopMatrix, Rotate, Translate
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, NumericProperty, BooleanProperty

# Window settings
Window.size = (420, 750)
Window.clearcolor = (0.08, 0.08, 0.15, 1)

# Theme colors
THEME_COLORS = {
    "karma": [1, 0.44, 0.26, 1],
    "dharma": [0.3, 0.69, 0.31, 1],
    "jnana": [0.13, 0.59, 0.95, 1],
    "bhakti": [0.91, 0.12, 0.39, 1],
    "yoga": [0.61, 0.15, 0.69, 1],
    "meditation": [0, 0.74, 0.83, 1]
}

THEME_ICONS = {
    "karma": "⚡",
    "dharma": "⚖️",
    "jnana": "📚",
    "bhakti": "❤️",
    "yoga": "🧘",
    "meditation": "🕉️"
}

LIFE_SITUATIONS = {
    "stress": {"icon": "😰", "label": "Stress Relief", "color": [0.4, 0.7, 1, 1]},
    "success": {"icon": "🏆", "label": "Success", "color": [1, 0.8, 0, 1]},
    "relationships": {"icon": "❤️", "label": "Relationships", "color": [1, 0.4, 0.6, 1]},
    "decision_making": {"icon": "🤔", "label": "Decisions", "color": [0.7, 0.4, 1, 1]},
    "peace": {"icon": "🕊️", "label": "Inner Peace", "color": [0.4, 1, 0.8, 1]},
    "motivation": {"icon": "🔥", "label": "Motivation", "color": [1, 0.5, 0.2, 1]},
    "fear": {"icon": "😨", "label": "Overcoming Fear", "color": [0.6, 0.6, 0.8, 1]},
    "grief": {"icon": "😢", "label": "Healing", "color": [0.7, 0.7, 1, 1]},
    "anger": {"icon": "😤", "label": "Managing Anger", "color": [1, 0.3, 0.3, 1]},
    "gratitude": {"icon": "🙏", "label": "Gratitude", "color": [1, 0.9, 0.4, 1]},
    "focus": {"icon": "🎯", "label": "Focus", "color": [0.3, 0.8, 0.5, 1]},
    "purpose": {"icon": "🌟", "label": "Life Purpose", "color": [0.9, 0.7, 1, 1]}
}

class ThemeManager:
    DARK_THEME = {
        'background': (0.08, 0.08, 0.15, 1),
        'text_primary': (1, 1, 1, 1),
        'text_secondary': (0.7, 0.7, 0.7, 1),
        'stat_bg': (0.2, 0.2, 0.3, 1),
    }
    
    LIGHT_THEME = {
        'background': (0.95, 0.93, 0.88, 1),
        'text_primary': (0.1, 0.1, 0.1, 1),
        'text_secondary': (0.4, 0.4, 0.4, 1),
        'stat_bg': (0.85, 0.82, 0.75, 1),
    }
    
    @staticmethod
    def get_theme(theme_name='dark'):
        if theme_name == 'light':
            return ThemeManager.LIGHT_THEME
        return ThemeManager.DARK_THEME

class GradientBackground(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color1 = [0.08, 0.08, 0.15, 1]
        self.color2 = [0.15, 0.08, 0.25, 1]
        self.time_val = 0
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        Clock.schedule_interval(self.animate_gradient, 1/30)
        self.update_canvas()
    
    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            num_steps = 20
            for i in range(num_steps):
                ratio = i / num_steps
                color = self.interpolate_color(self.color1, self.color2, ratio)
                Color(*color)
                Rectangle(pos=(self.x, self.y + (self.height * ratio)), size=(self.width, self.height / num_steps + 1))
    
    def interpolate_color(self, c1, c2, ratio):
        return [c1[0] + (c2[0] - c1[0]) * ratio, c1[1] + (c2[1] - c1[1]) * ratio, c1[2] + (c2[2] - c1[2]) * ratio, 1]
    
    def animate_gradient(self, dt):
        self.time_val += dt
        self.color1 = [0.08 + 0.03 * math.sin(self.time_val * 0.5), 0.08 + 0.03 * math.sin(self.time_val * 0.7), 0.15 + 0.05 * math.sin(self.time_val * 0.3), 1]
        self.color2 = [0.15 + 0.05 * math.sin(self.time_val * 0.4 + 2), 0.08 + 0.03 * math.sin(self.time_val * 0.6 + 1), 0.25 + 0.05 * math.sin(self.time_val * 0.5 + 3), 1]
        self.update_canvas()

class FloatingOm(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(40), dp(40))
        self.opacity = random.uniform(0.2, 0.5)
        self.rotation = random.randint(0, 360)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.update_canvas()
        self.animate_float()
    
    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            PushMatrix()
            Translate(self.center_x, self.center_y)
            Rotate(angle=self.rotation)
            Color(0.9, 0.72, 0, self.opacity)
            Label(text="ॐ", font_size=self.width, color=(0.9, 0.72, 0, self.opacity), pos=(-self.width/2, -self.height/2), size=self.size)
            PopMatrix()
    
    def animate_float(self):
        anim = Animation(pos=(self.x, self.y + dp(100)), opacity=0, duration=random.uniform(5, 8))
        anim.bind(on_complete=self.reset_position)
        anim.start(self)
    
    def reset_position(self, *args):
        self.pos = (random.randint(0, int(Window.width) - dp(40)), -dp(40))
        self.opacity = random.uniform(0.2, 0.5)
        self.animate_float()

class RippleEffect(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ripples = []
    
    def add_ripple(self, x, y):
        ripple = {'x': x, 'y': y, 'radius': dp(10), 'opacity': 0.5, 'max_radius': dp(150)}
        self.ripples.append(ripple)
        Clock.schedule_interval(self.update_ripples, 1/60)
    
    def update_ripples(self, dt):
        self.canvas.clear()
        alive = False
        with self.canvas:
            for ripple in self.ripples:
                if ripple['radius'] < ripple['max_radius']:
                    ripple['radius'] += dp(5)
                    ripple['opacity'] -= 0.01
                    Color(0.9, 0.72, 0, ripple['opacity'])
                    Line(circle=(ripple['x'], ripple['y'], ripple['radius']), width=dp(2))
                    alive = True
        if not alive:
            Clock.unschedule(self.update_ripples)

class GlowingBorder(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.glow_alpha = 0.3
        Clock.schedule_interval(self.animate_glow, 1/30)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
    
    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0.9, 0.72, 0, self.glow_alpha * 0.5)
            RoundedRectangle(pos=(self.x - dp(5), self.y - dp(5)), size=(self.width + dp(10), self.height + dp(10)), radius=[dp(20)])
            Color(0.9, 0.72, 0, self.glow_alpha)
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(15)), width=dp(2))
    
    def animate_glow(self, dt):
        self.glow_alpha = 0.3 + 0.2 * math.sin(time.time() * 2)
        self.update_canvas()

class ParticleExplosion(Widget):
    def __init__(self, center_x, center_y, **kwargs):
        super().__init__(**kwargs)
        self.particles = []
        for i in range(20):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(dp(2), dp(8))
            particle = {'x': center_x, 'y': center_y, 'vx': math.cos(angle) * speed, 'vy': math.sin(angle) * speed, 'life': 1.0, 'color': random.choice([(1, 0.85, 0.3, 1), (1, 0.6, 0.2, 1), (1, 0.9, 0.5, 1), (0.9, 0.72, 0, 1)])}
            self.particles.append(particle)
        Clock.schedule_interval(self.update_particles, 1/60)
    
    def update_particles(self, dt):
        self.canvas.clear()
        alive = False
        with self.canvas:
            for p in self.particles:
                if p['life'] > 0:
                    p['x'] += p['vx']
                    p['y'] += p['vy']
                    p['vy'] -= dp(0.2)
                    p['life'] -= 0.02
                    Color(*p['color'][:3], p['life'])
                    size = dp(4) * p['life']
                    Ellipse(pos=(p['x'] - size/2, p['y'] - size/2), size=(size, size))
                    alive = True
        if not alive:
            Clock.unschedule(self.update_particles)
            if self.parent:
                self.parent.remove_widget(self)

class CardBackDesign(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(300), dp(400))
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.update_canvas()
    
    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0.85, 0.65, 0.13, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(20)])
            Color(0.95, 0.78, 0.25, 0.3)
            RoundedRectangle(pos=(self.x + dp(15), self.y + dp(15)), size=(self.width - dp(30), self.height - dp(30)), radius=[dp(15)])
            Color(0.08, 0.08, 0.15, 0.7)
            Line(rounded_rectangle=(self.x + dp(10), self.y + dp(10), self.width - dp(20), self.height - dp(20), dp(15)), width=dp(2))
            for offset in [dp(25), dp(40)]:
                Color(0.9, 0.72, 0, 0.4)
                Line(rounded_rectangle=(self.x + offset, self.y + offset, self.width - (offset * 2), self.height - (offset * 2), dp(10)), width=dp(1))
            feather_positions = [(self.x + dp(30), self.y + self.height - dp(50)), (self.x + self.width - dp(50), self.y + self.height - dp(50)), (self.x + dp(30), self.y + dp(30)), (self.x + self.width - dp(50), self.y + dp(30))]
            for fx, fy in feather_positions:
                Color(0.1, 0.4, 0.6, 0.5)
                Ellipse(pos=(fx, fy), size=(dp(20), dp(30)))
                Color(0.2, 0.6, 0.3, 0.5)
                Ellipse(pos=(fx + dp(5), fy + dp(8)), size=(dp(10), dp(15)))

class GoldenPattern(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(300), dp(400))
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.update_canvas()
    
    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0.9, 0.72, 0, 0.6)
            Line(rounded_rectangle=(self.x + dp(10), self.y + dp(10), self.width - dp(20), self.height - dp(20), dp(15)), width=dp(1))
            Color(0.9, 0.72, 0, 0.3)
            Line(rounded_rectangle=(self.x + dp(20), self.y + dp(20), self.width - dp(40), self.height - dp(40), dp(12)), width=dp(1))
            for i in range(6):
                for j in range(8):
                    x = self.x + dp(40) + (i * dp(45))
                    y = self.y + dp(40) + (j * dp(45))
                    Color(0.9, 0.72, 0, 0.15)
                    Ellipse(pos=(x, y), size=(dp(3), dp(3)))
            corners = [(self.x + dp(20), self.y + dp(20)), (self.x + self.width - dp(35), self.y + dp(20)), (self.x + dp(20), self.y + self.height - dp(35)), (self.x + self.width - dp(35), self.y + self.height - dp(35))]
            for cx, cy in corners:
                Color(0.9, 0.72, 0, 0.5)
                Ellipse(pos=(cx, cy), size=(dp(15), dp(15)))
                Color(0.08, 0.08, 0.15, 0.5)
                Ellipse(pos=(cx + dp(3), cy + dp(3)), size=(dp(9), dp(9)))

class StarParticle(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(8), dp(8))
        self.opacity = random.uniform(0.3, 1)
        self.twinkle_speed = random.uniform(0.5, 2)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.update_canvas()
    
    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 0.8, self.opacity)
            Ellipse(pos=self.pos, size=self.size)
            Color(1, 1, 0.8, self.opacity * 0.3)
            Ellipse(pos=(self.x - dp(2), self.y - dp(2)), size=(self.width + dp(4), self.height + dp(4)))

class DiyaParticle(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(30), dp(30))
        self.opacity = random.uniform(0.6, 1)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.update_canvas()
        self.animate_float()
    
    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0.6, 0.4, 0.2, self.opacity)
            Ellipse(pos=(self.x + dp(5), self.y), size=(dp(20), dp(10)))
            Color(1, 0.5, 0, self.opacity * 0.8)
            Ellipse(pos=(self.x + dp(10), self.y + dp(8)), size=(dp(10), dp(15)))
            Color(1, 0.8, 0.2, self.opacity)
            Ellipse(pos=(self.x + dp(12), self.y + dp(10)), size=(dp(6), dp(10)))
            Color(1, 0.6, 0.1, self.opacity * 0.3)
            Ellipse(pos=(self.x + dp(5), self.y + dp(3)), size=(dp(20), dp(25)))
    
    def animate_float(self):
        anim = Animation(pos=(self.x, self.y + dp(20)), duration=random.uniform(3, 5)) + Animation(pos=self.pos, duration=random.uniform(3, 5))
        anim.repeat = True
        anim.start(self)

class ParticleSystem(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.particles = []
        self.setup_particles()
        Clock.schedule_interval(self.animate_particles, 1/30)
    
    def setup_particles(self):
        screen_width = int(Window.width)
        screen_height = int(Window.height)
        diya_size = int(dp(30))
        for i in range(15):
            star_x = random.randint(0, screen_width)
            star_y = random.randint(0, screen_height)
            star = StarParticle(pos=(star_x, star_y))
            self.add_widget(star)
            self.particles.append(star)
        for i in range(5):
            diya_x = random.randint(0, max(0, screen_width - diya_size))
            diya_y = random.randint(0, max(0, screen_height - diya_size))
            diya = DiyaParticle(pos=(diya_x, diya_y))
            self.add_widget(diya)
            self.particles.append(diya)
    
    def animate_particles(self, dt):
        for particle in self.particles:
            if isinstance(particle, StarParticle):
                particle.opacity = 0.3 + 0.7 * abs(math.sin(time.time() * particle.twinkle_speed))

class BackgroundMusic:
    _music = None
    _is_playing = False
    _volume = 0.7
    
    @classmethod
    def load(cls):
        music_files = ['flute.mp3', 'om.mp3', 'background.mp3', 'music.mp3']
        for file in music_files:
            if os.path.exists(file):
                try:
                    cls._music = SoundLoader.load(file)
                    if cls._music:
                        cls._music.loop = True
                        cls._music.volume = cls._volume
                        print(f"✅ Music loaded: {file}")
                        return True
                except Exception as e:
                    print(f"❌ Error loading music: {e}")
        return False
    
    @classmethod
    def play(cls):
        if cls._music is None:
            cls.load()
        if cls._music and not cls._is_playing:
            try:
                cls._music.volume = cls._volume
                cls._music.play()
                cls._is_playing = True
            except:
                pass
    
    @classmethod
    def pause(cls):
        if cls._music and cls._is_playing:
            try:
                cls._music.stop()
                cls._is_playing = False
            except:
                pass
    
    @classmethod
    def toggle(cls):
        if cls._is_playing:
            cls.pause()
        else:
            cls.play()
        return cls._is_playing

class PeacockFeather(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(30), dp(30))
        self.angle = random.randint(0, 360)
        self.opacity = random.uniform(0.3, 0.7)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.update_canvas()
        self.animate_float()
    
    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            PushMatrix()
            Translate(self.center_x, self.center_y)
            Rotate(angle=self.angle)
            Color(0.1, 0.4, 0.6, self.opacity)
            Ellipse(pos=(-dp(8), -dp(15)), size=(dp(16), dp(30)))
            Color(0.2, 0.6, 0.3, self.opacity)
            Ellipse(pos=(-dp(5), -dp(12)), size=(dp(10), dp(24)))
            Color(0.8, 0.6, 0.1, self.opacity)
            Ellipse(pos=(-dp(3), -dp(8)), size=(dp(6), dp(16)))
            PopMatrix()
    
    def animate_float(self):
        anim = Animation(pos=(self.x + random.randint(-20, 20), self.y + random.randint(-30, 30)), duration=random.uniform(2, 4)) + Animation(pos=self.pos, duration=random.uniform(2, 4))
        anim.repeat = True
        anim.start(self)

class LotusFlower(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(50), dp(50))
        self.opacity = random.uniform(0.5, 0.9)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.update_canvas()
        self.animate_pulse()
    
    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            for i in range(8):
                angle = i * 45
                PushMatrix()
                Translate(self.center_x, self.center_y)
                Rotate(angle=angle)
                Color(1, 0.7, 0.8, self.opacity)
                Ellipse(pos=(dp(-5), dp(5)), size=(dp(10), dp(20)))
                PopMatrix()
            Color(1, 0.85, 0.3, self.opacity)
            Ellipse(pos=(self.center_x - dp(8), self.center_y - dp(8)), size=(dp(16), dp(16)))
    
    def animate_pulse(self):
        anim = Animation(opacity=0.3, duration=2) + Animation(opacity=0.9, duration=2)
        anim.repeat = True
        anim.start(self)

class DivineGlow(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(200), dp(200))
        self.opacity = 0.3
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.update_canvas()
        self.animate_glow()
    
    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(1, 0.85, 0.3, self.opacity * 0.3)
            Ellipse(pos=self.pos, size=self.size)
            Color(1, 0.85, 0.3, self.opacity * 0.5)
            Ellipse(pos=(self.x + dp(30), self.y + dp(30)), size=(self.width - dp(60), self.height - dp(60)))
            Color(1, 0.9, 0.5, self.opacity)
            Ellipse(pos=(self.x + dp(60), self.y + dp(60)), size=(self.width - dp(120), self.height - dp(120)))
    
    def animate_glow(self):
        anim = Animation(opacity=0.1, duration=3) + Animation(opacity=0.5, duration=3)
        anim.repeat = True
        anim.start(self)

class KrishnaSilhouette(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(150), dp(200))
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.update_canvas()
    
    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0.1, 0.3, 0.6, 1)
            Ellipse(pos=(self.x + dp(50), self.y + dp(150)), size=(dp(50), dp(50)))
            Color(0.2, 0.5, 0.3, 1)
            Ellipse(pos=(self.x + dp(65), self.y + dp(180)), size=(dp(20), dp(40)))
            Color(0.1, 0.4, 0.6, 1)
            Ellipse(pos=(self.x + dp(68), self.y + dp(185)), size=(dp(14), dp(30)))
            Color(0.8, 0.6, 0.1, 1)
            Ellipse(pos=(self.x + dp(70), self.y + dp(190)), size=(dp(10), dp(20)))
            Color(0.1, 0.3, 0.6, 1)
            RoundedRectangle(pos=(self.x + dp(45), self.y + dp(50)), size=(dp(60), dp(110)), radius=[dp(30)])
            Color(0.9, 0.7, 0.1, 1)
            RoundedRectangle(pos=(self.x + dp(45), self.y + dp(20)), size=(dp(60), dp(40)), radius=[dp(20)])
            Color(0.6, 0.4, 0.2, 1)
            Line(points=[self.x + dp(75), self.y + dp(70), self.x + dp(100), self.y + dp(85)], width=dp(3))
            Color(0.8, 0.6, 0.1, 1)
            Triangle(points=[self.x + dp(50), self.y + dp(200), self.x + dp(75), self.y + dp(220), self.x + dp(100), self.y + dp(200)])

class AnimatedBackground(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_background()
    
    def setup_background(self):
        screen_width = int(Window.width)
        screen_height = int(Window.height)
        glow_x = int(Window.width/2 - dp(100))
        glow_y = int(Window.height/2 - dp(100))
        self.glow = DivineGlow(pos=(glow_x, glow_y))
        self.add_widget(self.glow)
        for i in range(5):
            lotus_x = random.randint(0, max(0, screen_width - int(dp(50))))
            lotus_y = random.randint(0, max(0, screen_height - int(dp(50))))
            lotus = LotusFlower(pos=(lotus_x, lotus_y))
            self.add_widget(lotus)
        for i in range(8):
            feather_x = random.randint(0, max(0, screen_width - int(dp(30))))
            feather_y = random.randint(0, max(0, screen_height - int(dp(30))))
            feather = PeacockFeather(pos=(feather_x, feather_y))
            self.add_widget(feather)

class GradientButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.color = (0.1, 0.1, 0.18, 1)
        self.font_size = 18
        self.bold = True
        self.size_hint_y = None
        self.height = dp(55)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.update_canvas()
        self.bind(on_press=self.on_press_anim, on_release=self.on_release_anim)
    
    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 0.4)
            RoundedRectangle(pos=(self.x + 3, self.y - 3), size=self.size, radius=[dp(15)])
            Color(0.9, 0.72, 0, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])
            Color(1, 0.85, 0.3, 0.3)
            RoundedRectangle(pos=(self.x + 5, self.y + self.height/2), size=(self.width - 10, self.height/2 - 5), radius=[dp(12)])
    
    def on_press_anim(self, *args):
        anim = Animation(height=dp(50), duration=0.1)
        anim.start(self)
    
    def on_release_anim(self, *args):
        anim = Animation(height=dp(55), duration=0.1)
        anim.start(self)

class StatCard(BoxLayout):
    def __init__(self, value="0", label="", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(5)
        with self.canvas.before:
            Color(0.2, 0.2, 0.3, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
            Color(0.9, 0.72, 0, 0.5)
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(10)), width=1)
        self.bind(pos=self.update_rect, size=self.update_rect)
        value_label = Label(text=value, font_size=28, bold=True, color=get_color_from_hex('#e6b800'))
        text_label = Label(text=label, font_size=12, color=(0.7, 0.7, 0.7, 1))
        self.add_widget(value_label)
        self.add_widget(text_label)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()
    
    def setup_ui(self):
        main_layout = FloatLayout()
        with main_layout.canvas.before:
            Color(0.08, 0.08, 0.15, 1)
            self.bg_rect = Rectangle(pos=main_layout.pos, size=main_layout.size)
        main_layout.bind(pos=self.update_bg, size=self.update_bg)
        self.gradient_bg = GradientBackground()
        main_layout.add_widget(self.gradient_bg)
        self.particles = ParticleSystem()
        main_layout.add_widget(self.particles)
        self.floating_oms = []
        for i in range(5):
            om = FloatingOm(pos=(random.randint(0, int(Window.width)), random.randint(0, int(Window.height))))
            self.floating_oms.append(om)
            main_layout.add_widget(om)
        self.ripple = RippleEffect()
        main_layout.add_widget(self.ripple)
        
        content = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(8), size_hint=(1, 1))
        top_bar = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(5))
        icon_label = Label(text="🕉️", font_size=25, size_hint_x=None, width=dp(35), color=get_color_from_hex('#e6b800'))
        top_bar.add_widget(icon_label)
        theme_btn = Button(text="🌓", font_size=18, size_hint_x=None, width=dp(35), background_normal='', background_color=(0, 0, 0, 0), color=(1, 1, 1, 1))
        theme_btn.bind(on_release=self.toggle_theme)
        top_bar.add_widget(theme_btn)
        music_btn = Button(text="🎵", font_size=18, size_hint_x=None, width=dp(35), background_normal='', background_color=(0, 0, 0, 0), color=(1, 1, 1, 1))
        music_btn.bind(on_release=self.toggle_music)
        top_bar.add_widget(music_btn)
        top_bar.add_widget(Widget())
        settings_btn = Button(text="⚙️", font_size=20, size_hint_x=None, width=dp(35), background_normal='', background_color=(0, 0, 0, 0), color=(1, 1, 1, 1))
        settings_btn.bind(on_release=self.open_settings)
        top_bar.add_widget(settings_btn)
        content.add_widget(top_bar)
        
        hero = FloatLayout(size_hint_y=None, height=dp(150))
        krishna_x = int(Window.width/2 - dp(60))
        krishna_y = int(dp(5))
        krishna = KrishnaSilhouette(pos=(krishna_x, krishna_y), size=(dp(120), dp(140)))
        hero.add_widget(krishna)
        glow_x = int(Window.width/2 - dp(80))
        glow_y = int(dp(0))
        glow = DivineGlow(pos=(glow_x, glow_y))
        hero.add_widget(glow)
        title = Label(text="GITA WISDOM", font_size=24, bold=True, color=get_color_from_hex('#e6b800'), pos_hint={'center_x': 0.5, 'top': 1}, size_hint_y=None, height=dp(30))
        hero.add_widget(title)
        subtitle = Label(text="Divine Guidance from Lord Krishna", font_size=12, color=(0.7, 0.7, 0.7, 1), pos_hint={'center_x': 0.5, 'y': 0}, size_hint_y=None, height=dp(18))
        hero.add_widget(subtitle)
        content.add_widget(hero)
        
        stats_row = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(8))
        app = App.get_running_app()
        stats_row.add_widget(StatCard(value=str(len(app.quotes)), label="Quotes"))
        stats_row.add_widget(StatCard(value=str(len(app.favorites)), label="Favorites"))
        stats_row.add_widget(StatCard(value=f"{app.get_streak()}🔥", label="Streak"))
        content.add_widget(stats_row)
        
        scroll = ScrollView(size_hint_y=1)
        btn_container = BoxLayout(orientation='vertical', spacing=dp(8), size_hint_y=None, padding=dp(5))
        btn_container.bind(minimum_height=btn_container.setter('height'))
        buttons_data = [("📿 Daily Gita", self.show_daily), ("🎴 Draw a Card", self.go_to_card), ("🌟 Mood-Based Quotes", self.go_to_mood), ("❤️ My Favorites", self.go_to_favorites), ("🔍 Search Quotes", self.go_to_search), ("🧘 Meditation Timer", self.go_to_meditation)]
        for text, callback in buttons_data:
            btn = GradientButton(text=text)
            btn.bind(on_release=callback)
            btn_container.add_widget(btn)
        scroll.add_widget(btn_container)
        content.add_widget(scroll)
        main_layout.add_widget(content)
        self.add_widget(main_layout)
    
    def on_touch_down(self, touch):
        if hasattr(self, 'ripple'):
            self.ripple.add_ripple(touch.x, touch.y)
        return super().on_touch_down(touch)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def toggle_theme(self, instance):
        app = App.get_running_app()
        app.theme = 'light' if app.theme == 'dark' else 'dark'
        app.apply_theme()
        instance.text = '☀️' if app.theme == 'light' else '🌓'
        theme_colors = ThemeManager.get_theme(app.theme)
        self.bg_rect.rgba = theme_colors['background']
    
    def toggle_music(self, instance):
        is_playing = BackgroundMusic.toggle()
        instance.text = '🔊' if is_playing else '🎵'
    
    def show_daily(self, instance):
        random.seed(datetime.now().strftime("%Y%m%d"))
        quote = random.choice(App.get_running_app().quotes)
        random.seed(None)
        self.manager.get_screen('card').display_quote(quote)
        self.manager.current = 'card'
        App.get_running_app().update_streak()
    
    def go_to_card(self, instance):
        self.manager.current = 'card'
    
    def go_to_mood(self, instance):
        self.manager.current = 'mood'
    
    def go_to_favorites(self, instance):
        self.manager.current = 'favorites'
    
    def go_to_search(self, instance):
        self.manager.current = 'search'
    
    def go_to_meditation(self, instance):
        self.manager.current = 'meditation'
    
    def open_settings(self, instance):
        self.manager.current = 'settings'

class CardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_quote = None
        self.is_flipped = False
        self._swipe_start_x = 0
        self._is_animating = False
        self.setup_ui()
    
    def setup_ui(self):
        layout = FloatLayout()
        with layout.canvas.before:
            Color(0.08, 0.08, 0.15, 1)
            self.bg_rect = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=self.update_bg, size=self.update_bg)
        self.gradient_bg = GradientBackground()
        layout.add_widget(self.gradient_bg)
        
        top_bar = BoxLayout(size_hint=(1, None), height=dp(50), padding=dp(10), spacing=dp(10), pos_hint={'top': 1})
        btn_back = Button(text="←", font_size=24, size_hint_x=None, width=dp(50), background_normal='', background_color=(0, 0, 0, 0), color=(1, 1, 1, 1))
        btn_back.bind(on_release=self.go_back)
        top_bar.add_widget(btn_back)
        title = Label(text="🕉️ Divine Cards 🕉️", font_size=20, bold=True, color=get_color_from_hex('#e6b800'))
        top_bar.add_widget(title)
        layout.add_widget(top_bar)
        
        self.card_area = FloatLayout(size_hint=(1, None), height=dp(430), pos_hint={'center_y': 0.5})
        
        glow = DivineGlow(pos=(int(Window.width/2 - dp(100)), int(dp(140))))
        self.card_area.add_widget(glow)
        
        self.card_back = Button(text="", size_hint=(None, None), size=(dp(300), dp(400)), pos_hint={'center_x': 0.5, 'center_y': 0.5}, background_normal='', background_color=(0, 0, 0, 0))
        self.card_back.bind(on_release=self.flip_card)
        
        self.card_back_design = CardBackDesign(pos=(self.card_back.x, self.card_back.y))
        self.card_back.add_widget(self.card_back_design)
        
        om_label = Label(text="ॐ", font_size=80, color=(0.08, 0.08, 0.15, 1), pos_hint={'center_x': 0.5, 'center_y': 0.6}, size_hint=(None, None), size=(dp(100), dp(100)))
        self.card_back.add_widget(om_label)
        
        tap_label = Label(text="Tap to Reveal\nDivine Wisdom", font_size=16, color=(0.08, 0.08, 0.15, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.2}, size_hint=(None, None), size=(dp(200), dp(50)), halign='center')
        self.card_back.add_widget(tap_label)
        
        self.glow_border = GlowingBorder(pos=(self.card_back.x - dp(8), self.card_back.y - dp(8)), size=(self.card_back.width + dp(16), self.card_back.height + dp(16)))
        self.card_area.add_widget(self.glow_border)
        
        self.card_front = BoxLayout(orientation='vertical', size_hint=(None, None), size=(dp(300), dp(400)), pos_hint={'center_x': 0.5, 'center_y': 0.5}, padding=dp(20), spacing=dp(10), opacity=0)
        with self.card_front.canvas.before:
            Color(1, 1, 1, 1)
            self.card_rect = RoundedRectangle(pos=self.card_front.pos, size=self.card_front.size, radius=[dp(20)])
        self.card_front.bind(pos=self.update_card_rect, size=self.update_card_rect)
        
        self.card_pattern = GoldenPattern(pos=(self.card_front.x, self.card_front.y))
        self.card_front.add_widget(self.card_pattern)
        
        self.theme_label = Label(text="", size_hint_y=None, height=dp(40), bold=True, font_size=14, color=(0, 0, 0, 1))
        self.sanskrit_label = Label(text="", size_hint_y=None, height=dp(90), color=(0.2, 0.2, 0.2, 1), font_size=12, text_size=(dp(250), None), halign='center', valign='middle')
        
        separator = Widget(size_hint_y=None, height=dp(1))
        with separator.canvas:
            Color(0.9, 0.72, 0, 0.3)
            Line(points=[dp(50), 0, dp(250), 0], width=dp(1))
        
        self.translation_label = Label(text="", size_hint_y=None, height=dp(100), color=(0.4, 0.4, 0.4, 1), italic=True, font_size=12, text_size=(dp(250), None), halign='center', valign='middle')
        self.ref_label = Label(text="", size_hint_y=None, height=dp(25), bold=True, font_size=12, color=(0, 0, 0, 1))
        self.interpretation_label = Label(text="", size_hint_y=None, height=dp(60), color=(0.5, 0.5, 0.5, 1), font_size=10, text_size=(dp(250), None), halign='center')
        
        self.card_front.add_widget(self.theme_label)
        self.card_front.add_widget(self.sanskrit_label)
        self.card_front.add_widget(separator)
        self.card_front.add_widget(self.translation_label)
        self.card_front.add_widget(self.ref_label)
        self.card_front.add_widget(self.interpretation_label)
        
        self.card_area.add_widget(self.card_back)
        self.card_area.add_widget(self.card_front)
        layout.add_widget(self.card_area)
        
        bottom_layout = BoxLayout(size_hint=(1, None), height=dp(110), padding=dp(15), spacing=dp(8), pos_hint={'y': 0}, orientation='vertical')
        self.btn_action = GradientButton(text="Tap Card to Flip")
        self.btn_action.bind(on_release=self.flip_card)
        bottom_layout.add_widget(self.btn_action)
        
        btn_row = BoxLayout(spacing=dp(8))
        btn_save = GradientButton(text="❤️ Save")
        btn_save.bind(on_release=self.save_to_fav)
        btn_row.add_widget(btn_save)
        btn_share = GradientButton(text="📤 Share")
        btn_share.bind(on_release=self.share_quote)
        btn_row.add_widget(btn_share)
        btn_new = GradientButton(text="🔄 New")
        btn_new.bind(on_release=self.new_card)
        btn_row.add_widget(btn_new)
        bottom_layout.add_widget(btn_row)
        layout.add_widget(bottom_layout)
        
        self.add_widget(layout)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def update_card_rect(self, *args):
        self.card_rect.pos = self.card_front.pos
        self.card_rect.size = self.card_front.size
        if hasattr(self, 'card_pattern'):
            self.card_pattern.pos = self.card_front.pos
            self.card_pattern.size = self.card_front.size
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._swipe_start_x = touch.x
        return super().on_touch_down(touch)
    
    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos) and not self._is_animating:
            dx = touch.x - self._swipe_start_x
            # Only rotate card_back (Button supports rotation)
            if not self.is_flipped and hasattr(self.card_back, 'rotation'):
                self.card_back.rotation = dx * 0.05
            
            if abs(dx) > dp(80):
                self.animate_swipe_card(dx)
                return True
        return super().on_touch_move(touch)
    
    def on_touch_up(self, touch):
        # Smoothly reset rotation - only for card_back which is a Button
        if hasattr(self, 'card_back') and hasattr(self.card_back, 'rotation'):
            anim = Animation(rotation=0, duration=0.4, t='out_elastic')
            anim.start(self.card_back)
        return super().on_touch_up(touch)
    
    def animate_swipe_card(self, direction):
        if self._is_animating:
            return
        self._is_animating = True
        target_x = int(Window.width) + dp(100) if direction > 0 else -dp(400)
        card = self.card_back if not self.is_flipped else self.card_front
        
        # Only apply rotation to Button widgets (card_back)
        if hasattr(card, 'rotation'):
            anim = Animation(
                pos=(target_x, card.y),
                opacity=0,
                rotation=direction * 0.2,
                duration=0.35,
                t='out_quad'
            )
        else:
            anim = Animation(
                pos=(target_x, card.y),
                opacity=0,
                duration=0.35,
                t='out_quad'
            )
        
        def after_swipe(*args):
            card.pos = (int(Window.width/2 - dp(150)), card.y)
            if hasattr(card, 'rotation'):
                card.rotation = 0
            self.display_quote(random.choice(App.get_running_app().quotes))
            card.opacity = 1
            anim_in = Animation(opacity=1, duration=0.25, t='out_sine')
            anim_in.start(card)
            self._is_animating = False
        
        anim.bind(on_complete=after_swipe)
        anim.start(card)
    
    def display_quote(self, quote):
        self.current_quote = quote
        theme = quote['theme'].lower()
        icon = THEME_ICONS.get(theme, "")
        self.theme_label.text = f"{icon} {quote['theme'].upper()} {icon}"
        self.theme_label.color = THEME_COLORS.get(theme, [0.5, 0.5, 0.5, 1])
        self.sanskrit_label.text = quote.get('sanskrit', '')
        self.translation_label.text = f'"{quote.get("translation", "")}"'
        self.ref_label.text = f"Chapter {quote['chapter']} : Verse {quote['verse']}"
        self.interpretation_label.text = quote.get('interpretation', '')
        self.is_flipped = False
        self.card_front.opacity = 0
        self.card_front.size = (dp(300), dp(400))
        self.card_back.opacity = 1
        self.card_back.size = (dp(300), dp(400))
        self.btn_action.text = "Tap Card to Flip"
    
    def flip_card(self, instance):
        if self._is_animating:
            return
        if self.is_flipped:
            self.new_card(instance)
            return
        if not self.current_quote:
            self.display_quote(random.choice(App.get_running_app().quotes))
            return
        self._is_animating = True
        
        def stage1():
            anim = Animation(size=(dp(30), dp(400)), opacity=0.6, duration=0.12, t='in_out_sine')
            anim.bind(on_complete=lambda *a: stage2())
            anim.start(self.card_back)
        
        def stage2():
            self.card_back.opacity = 0
            self.card_back.size = (dp(300), dp(400))
            self.card_front.size = (dp(30), dp(400))
            self.card_front.opacity = 1
            self.is_flipped = True
            anim = Animation(size=(dp(300), dp(400)), duration=0.25, t='out_cubic')
            anim.bind(on_complete=lambda *a: stage3())
            anim.start(self.card_front)
        
        def stage3():
            self.btn_action.text = "Draw Again"
            explosion = ParticleExplosion(center_x=self.card_front.center_x, center_y=self.card_front.center_y)
            self.card_area.add_widget(explosion)
            anim = Animation(size=(dp(295), dp(395)), duration=0.06, t='out_quad') + Animation(size=(dp(300), dp(400)), duration=0.1, t='out_elastic')
            anim.start(self.card_front)
            self._is_animating = False
        
        stage1()
    
    def new_card(self, instance):
        if self._is_animating:
            return
        self._is_animating = True
        anim_fade = Animation(opacity=0, duration=0.15, t='out_sine')
        
        def reset_card(*args):
            self.display_quote(random.choice(App.get_running_app().quotes))
            self.card_back.opacity = 1
            self.card_back.size = (dp(300), dp(400))
            anim_in = Animation(opacity=1, duration=0.2, t='out_sine')
            anim_in.start(self.card_back)
            self._is_animating = False
        
        anim_fade.bind(on_complete=reset_card)
        anim_fade.start(self.card_front)
    
    def go_back(self, instance):
        self.manager.current = 'main'
    
    def save_to_fav(self, instance):
        if self.current_quote:
            app = App.get_running_app()
            if app.add_favorite(self.current_quote):
                self.show_popup("Success", "Quote saved! ❤️")
            else:
                self.show_popup("Already Saved", "Already in favorites!")
    
    def share_quote(self, instance):
        if self.current_quote:
            q = self.current_quote
            share_text = f"""🕉️ Bhagavad Gita Wisdom 🕉️\n\n{q.get('sanskrit', '')}\n\n"{q.get('translation', '')}"\n\n- Chapter {q['chapter']}, Verse {q['verse']}\nTheme: {q['theme'].upper()}\n\n{q.get('interpretation', '')}\n\n📱 Shared from Gita Wisdom App"""
            self.show_popup("Share Quote", share_text)
    
    def show_popup(self, title, content):
        popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        popup_label = Label(text=content, color=(0.1, 0.1, 0.18, 1), text_size=(dp(300), None), halign='center')
        close_btn = GradientButton(text="Close", size_hint=(None, None), size=(dp(150), dp(40)))
        close_btn.pos_hint = {'center_x': 0.5}
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_btn)
        popup = Popup(title=title, content=popup_layout, size_hint=(None, None), size=(dp(350), dp(400)), background='', background_color=(1, 1, 1, 1))
        close_btn.bind(on_release=popup.dismiss)
        popup.open()

class MoodScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()
    
    def setup_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        with layout.canvas.before:
            Color(0.08, 0.08, 0.15, 1)
            self.bg_rect = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=self.update_bg, size=self.update_bg)
        title = Label(text="🌟 How Are You Feeling?", font_size=24, bold=True, color=get_color_from_hex('#e6b800'), size_hint_y=None, height=dp(60))
        layout.add_widget(title)
        scroll = ScrollView()
        mood_grid = GridLayout(cols=2, spacing=dp(10), padding=dp(10), size_hint_y=None)
        mood_grid.bind(minimum_height=mood_grid.setter('height'))
        for situation_key, situation_data in LIFE_SITUATIONS.items():
            btn = Button(text=f"{situation_data['icon']} {situation_data['label']}", size_hint_y=None, height=dp(60), background_normal='', background_color=situation_data['color'][:3] + [0.8], color=(0.1, 0.1, 0.18, 1), bold=True, font_size=14)
            btn.bind(on_release=lambda x, k=situation_key: self.show_mood_quote(k))
            mood_grid.add_widget(btn)
        scroll.add_widget(mood_grid)
        layout.add_widget(scroll)
        btn_back = GradientButton(text="← Back")
        btn_back.bind(on_release=self.go_back)
        layout.add_widget(btn_back)
        self.add_widget(layout)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def show_mood_quote(self, situation):
        app = App.get_running_app()
        matching_quotes = [q for q in app.quotes if q.get('life_situation') == situation]
        if matching_quotes:
            quote = random.choice(matching_quotes)
        else:
            quote = random.choice(app.quotes)
        self.manager.get_screen('card').display_quote(quote)
        self.manager.current = 'card'
    
    def go_back(self, instance):
        self.manager.current = 'main'

class FavoritesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()
    
    def setup_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        with layout.canvas.before:
            Color(0.08, 0.08, 0.15, 1)
            self.bg_rect = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=self.update_bg, size=self.update_bg)
        title = Label(text="❤️ My Favorites", font_size=24, bold=True, color=get_color_from_hex('#e6b800'), size_hint_y=None, height=dp(50))
        layout.add_widget(title)
        self.fav_list = BoxLayout(orientation='vertical', spacing=8, size_hint_y=None)
        self.fav_list.bind(minimum_height=self.fav_list.setter('height'))
        scroll = ScrollView(size_hint_y=0.8)
        scroll.add_widget(self.fav_list)
        layout.add_widget(scroll)
        btn_layout = BoxLayout(spacing=10, size_hint_y=None, height=dp(50))
        btn_home = GradientButton(text="← Home")
        btn_home.bind(on_release=self.go_home)
        btn_layout.add_widget(btn_home)
        btn_clear = GradientButton(text="🗑️ Clear All")
        btn_clear.bind(on_release=self.clear_favorites)
        btn_layout.add_widget(btn_clear)
        layout.add_widget(btn_layout)
        self.add_widget(layout)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def on_enter(self):
        self.refresh_favorites()
    
    def refresh_favorites(self):
        self.fav_list.clear_widgets()
        favorites = App.get_running_app().favorites
        if not favorites:
            empty_label = Label(text="No favorites yet\n\nTap ❤️ on a quote to save it", color=(0.7, 0.7, 0.7, 1), size_hint_y=None, height=dp(100))
            self.fav_list.add_widget(empty_label)
        else:
            for quote in favorites:
                btn = Button(text=f"Chapter {quote['chapter']}:{quote['verse']}\n{quote['translation'][:80]}...", size_hint_y=None, height=dp(80), background_normal='', background_color=(0.2, 0.2, 0.3, 1), color=(1, 1, 1, 1), halign='left', valign='middle', padding=(dp(10), dp(5)))
                btn.bind(on_release=lambda x, q=quote: self.show_quote_details(q))
                self.fav_list.add_widget(btn)
    
    def show_quote_details(self, quote):
        content = f"""🕉️ {quote.get('sanskrit', '')}\n\n"{quote.get('translation', '')}"\n\n- Chapter {quote['chapter']}, Verse {quote['verse']}\nTheme: {quote['theme'].upper()}\n\n{quote.get('interpretation', '')}"""
        popup = Popup(title=f"Chapter {quote['chapter']}:{quote['verse']}", content=Label(text=content, color=(0.1, 0.1, 0.18, 1)), size_hint=(None, None), size=(dp(350), dp(450)), background='', background_color=(1, 1, 1, 1))
        popup.open()
    
    def clear_favorites(self, instance):
        app = App.get_running_app()
        app.favorites = []
        app.save_favorites()
        self.refresh_favorites()
    
    def go_home(self, instance):
        self.manager.current = 'main'

class SearchScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()
    
    def setup_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        with layout.canvas.before:
            Color(0.08, 0.08, 0.15, 1)
            self.bg_rect = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=self.update_bg, size=self.update_bg)
        title = Label(text="🔍 Search Quotes", font_size=24, bold=True, color=get_color_from_hex('#e6b800'), size_hint_y=None, height=dp(50))
        layout.add_widget(title)
        self.search_input = TextInput(hint_text="Search by theme, chapter, or keyword...", size_hint_y=None, height=dp(40), multiline=False, background_normal='', background_color=(0.2, 0.2, 0.3, 1), foreground_color=(1, 1, 1, 1), hint_text_color=(0.5, 0.5, 0.5, 1), padding=(dp(10), dp(10)))
        layout.add_widget(self.search_input)
        btn_search = GradientButton(text="Search")
        btn_search.bind(on_release=self.perform_search)
        layout.add_widget(btn_search)
        self.results_list = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        self.results_list.bind(minimum_height=self.results_list.setter('height'))
        scroll = ScrollView(size_hint_y=0.6)
        scroll.add_widget(self.results_list)
        layout.add_widget(scroll)
        btn_back = GradientButton(text="← Back")
        btn_back.bind(on_release=self.go_back)
        layout.add_widget(btn_back)
        self.add_widget(layout)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def perform_search(self, instance):
        query = self.search_input.text.lower().strip()
        if not query:
            return
        self.results_list.clear_widgets()
        quotes = App.get_running_app().quotes
        results = []
        for quote in quotes:
            if (query in quote['theme'].lower() or query in quote['translation'].lower() or query in quote.get('sanskrit', '').lower() or query == f"chapter {quote['chapter']}" or query == f"ch {quote['chapter']}"):
                results.append(quote)
        if not results:
            no_results = Label(text="No quotes found", color=(0.7, 0.7, 0.7, 1), size_hint_y=None, height=dp(50))
            self.results_list.add_widget(no_results)
        else:
            for quote in results[:20]:
                btn = Button(text=f"Ch {quote['chapter']}:{quote['verse']} - {quote['translation'][:50]}...", size_hint_y=None, height=dp(60), background_normal='', background_color=(0.2, 0.2, 0.3, 1), color=(1, 1, 1, 1), halign='left', valign='middle', padding=(dp(10), dp(5)))
                btn.bind(on_release=lambda x, q=quote: self.show_quote(q))
                self.results_list.add_widget(btn)
    
    def show_quote(self, quote):
        self.manager.get_screen('card').display_quote(quote)
        self.manager.current = 'card'
    
    def go_back(self, instance):
        self.manager.current = 'main'

class MeditationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timer_running = False
        self.seconds = 300
        self.setup_ui()
    
    def setup_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        with layout.canvas.before:
            Color(0.08, 0.08, 0.15, 1)
            self.bg_rect = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=self.update_bg, size=self.update_bg)
        title = Label(text="🧘 Meditation Timer", font_size=24, bold=True, color=get_color_from_hex('#e6b800'), size_hint_y=None, height=dp(50))
        layout.add_widget(title)
        self.timer_label = Label(text="05:00", font_size=60, bold=True, color=(1, 1, 1, 1), size_hint_y=None, height=dp(150))
        layout.add_widget(self.timer_label)
        self.quote_label = Label(text="Focus on your breath...", font_size=14, color=(0.7, 0.7, 0.7, 1), size_hint_y=None, height=dp(80), text_size=(dp(350), None), halign='center')
        layout.add_widget(self.quote_label)
        btn_layout = BoxLayout(spacing=10, size_hint_y=None, height=dp(50))
        btn_start = GradientButton(text="▶ Start")
        btn_start.bind(on_release=self.start_timer)
        btn_layout.add_widget(btn_start)
        btn_pause = GradientButton(text="⏸ Pause")
        btn_pause.bind(on_release=self.pause_timer)
        btn_layout.add_widget(btn_pause)
        btn_reset = GradientButton(text="🔄 Reset")
        btn_reset.bind(on_release=self.reset_timer)
        btn_layout.add_widget(btn_reset)
        layout.add_widget(btn_layout)
        duration_layout = BoxLayout(spacing=10, size_hint_y=None, height=dp(50))
        for duration in [1, 5, 10, 20]:
            btn = GradientButton(text=f"{duration} min")
            btn.bind(on_release=lambda x, d=duration: self.set_duration(d))
            duration_layout.add_widget(btn)
        layout.add_widget(duration_layout)
        btn_back = GradientButton(text="← Back")
        btn_back.bind(on_release=self.go_back)
        layout.add_widget(btn_back)
        self.add_widget(layout)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def set_duration(self, minutes):
        self.seconds = minutes * 60
        self.update_timer_display()
    
    def start_timer(self, instance):
        if not self.timer_running:
            self.timer_running = True
            Clock.schedule_interval(self.update_timer, 1)
    
    def pause_timer(self, instance):
        self.timer_running = False
        Clock.unschedule(self.update_timer)
    
    def reset_timer(self, instance):
        self.timer_running = False
        Clock.unschedule(self.update_timer)
        self.seconds = 300
        self.update_timer_display()
        self.quote_label.text = "Focus on your breath..."
    
    def update_timer(self, dt):
        if self.seconds > 0:
            self.seconds -= 1
            self.update_timer_display()
            if self.seconds % 30 == 0:
                quote = random.choice(App.get_running_app().quotes)
                self.quote_label.text = quote['translation']
        else:
            self.timer_running = False
            Clock.unschedule(self.update_timer)
            self.quote_label.text = "Meditation complete! 🕉️"
    
    def update_timer_display(self):
        minutes = self.seconds // 60
        seconds = self.seconds % 60
        self.timer_label.text = f"{minutes:02d}:{seconds:02d}"
    
    def go_back(self, instance):
        Clock.unschedule(self.update_timer)
        self.timer_running = False
        self.manager.current = 'main'

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()
    
    def setup_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        with layout.canvas.before:
            Color(0.08, 0.08, 0.15, 1)
            self.bg_rect = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=self.update_bg, size=self.update_bg)
        title = Label(text="⚙️ Settings", font_size=24, bold=True, color=get_color_from_hex('#e6b800'), size_hint_y=None, height=dp(50))
        layout.add_widget(title)
        notif_label = Label(text="Daily Notification Time", font_size=16, color=(1, 1, 1, 1), size_hint_y=None, height=dp(30))
        layout.add_widget(notif_label)
        self.time_input = TextInput(text=f"{App.get_running_app().notification_hour:02d}:{App.get_running_app().notification_minute:02d}", font_size=18, multiline=False, size_hint_y=None, height=dp(40), background_normal='', background_color=(0.2, 0.2, 0.3, 1), foreground_color=(1, 1, 1, 1), halign='center')
        layout.add_widget(self.time_input)
        btn_save = GradientButton(text="Save Settings")
        btn_save.bind(on_release=self.save_settings)
        layout.add_widget(btn_save)
        about_label = Label(text="\nGita Wisdom v3.0\n\nDivine app with 100+ quotes\nMood-Based Wisdom\nMeditation Timer\nBeautiful Animations\n\n🕉️ Made with ❤️", font_size=14, color=(0.7, 0.7, 0.7, 1), size_hint_y=None, height=dp(200))
        layout.add_widget(about_label)
        btn_back = GradientButton(text="← Back")
        btn_back.bind(on_release=self.go_back)
        layout.add_widget(btn_back)
        self.add_widget(layout)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def save_settings(self, instance):
        time_text = self.time_input.text
        try:
            hour, minute = map(int, time_text.split(':'))
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                app = App.get_running_app()
                app.notification_hour = hour
                app.notification_minute = minute
                app.save_settings()
                self.show_popup("Success", f"Notification set for {time_text}")
            else:
                self.show_popup("Error", "Invalid time format")
        except:
            self.show_popup("Error", "Use format HH:MM")
    
    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content, color=(0.1, 0.1, 0.18, 1)), size_hint=(None, None), size=(dp(300), dp(200)))
        popup.open()
    
    def go_back(self, instance):
        self.manager.current = 'main'

class GitaApp(App):
    quotes = []
    favorites = []
    notification_hour = 7
    notification_minute = 0
    theme = 'dark'
    
    def build(self):
        self.title = 'Gita Wisdom'
        self.load_data()
        self.load_settings()
        self.load_theme()
        BackgroundMusic.load()
        sm = ScreenManager()
        sm.transition.duration = 0.3
        sm.transition.type = 'fade'
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(CardScreen(name='card'))
        sm.add_widget(MoodScreen(name='mood'))
        sm.add_widget(FavoritesScreen(name='favorites'))
        sm.add_widget(SearchScreen(name='search'))
        sm.add_widget(MeditationScreen(name='meditation'))
        sm.add_widget(SettingsScreen(name='settings'))
        self.start_notification_service()
        self.apply_theme()
        Clock.schedule_once(lambda dt: BackgroundMusic.play(), 1)
        return sm
    
    def apply_theme(self):
        theme_colors = ThemeManager.get_theme(self.theme)
        Window.clearcolor = theme_colors['background']
    
    def load_theme(self):
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r') as f:
                    settings = json.load(f)
                    self.theme = settings.get('theme', 'dark')
        except:
            self.theme = 'dark'
    
    def load_settings(self):
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r') as f:
                    settings = json.load(f)
                    self.notification_hour = settings.get('hour', 7)
                    self.notification_minute = settings.get('minute', 0)
        except:
            pass
    
    def save_settings(self):
        try:
            with open('settings.json', 'w') as f:
                json.dump({'hour': self.notification_hour, 'minute': self.notification_minute, 'theme': self.theme}, f)
        except:
            pass
    
    def load_data(self):
        try:
            with open('quotes.json', 'r', encoding='utf-8') as f:
                self.quotes = json.load(f)
            print(f"✅ Loaded {len(self.quotes)} quotes")
        except:
            self.quotes = [{"chapter": 2, "verse": 47, "sanskrit": "कर्मण्येवाधिकारस्ते", "translation": "You have a right to perform your prescribed duties.", "theme": "karma"}]
        try:
            if os.path.exists('favorites.json'):
                with open('favorites.json', 'r') as f:
                    content = f.read().strip()
                    self.favorites = json.loads(content) if content else []
            else:
                self.favorites = []
        except:
            self.favorites = []
        self.streak = 0
        try:
            if os.path.exists('streak.json'):
                with open('streak.json', 'r') as f:
                    data = json.load(f)
                    last_date = data.get('last_date', '')
                    today = date.today().strftime("%Y-%m-%d")
                    if last_date == today:
                        self.streak = data.get('streak', 0)
                    elif last_date == (date.today() - timedelta(days=1)).strftime("%Y-%m-%d"):
                        self.streak = data.get('streak', 0)
        except:
            self.streak = 0
    
    def get_streak(self):
        return getattr(self, 'streak', 0)
    
    def update_streak(self):
        today = date.today().strftime("%Y-%m-%d")
        try:
            data = {}
            if os.path.exists('streak.json'):
                with open('streak.json', 'r') as f:
                    data = json.load(f)
            last_date = data.get('last_date', '')
            if last_date == today:
                return
            elif last_date == (date.today() - timedelta(days=1)).strftime("%Y-%m-%d"):
                self.streak = data.get('streak', 0) + 1
            else:
                self.streak = 1
            with open('streak.json', 'w') as f:
                json.dump({'last_date': today, 'streak': self.streak}, f)
        except:
            pass
    
    def add_favorite(self, quote):
        if quote not in self.favorites:
            self.favorites.append(quote)
            self.save_favorites()
            return True
        return False
    
    def save_favorites(self):
        try:
            with open('favorites.json', 'w', encoding='utf-8') as f:
                json.dump(self.favorites, f, indent=2)
        except:
            pass
    
    def start_notification_service(self):
        def check_time():
            while True:
                now = datetime.now()
                if (now.hour == self.notification_hour and now.minute == self.notification_minute):
                    quote = random.choice(self.quotes)
                    try:
                        from plyer import notification
                        notification.notify(title="🕉️ Gita Wisdom", message=f"Chapter {quote['chapter']}:{quote['verse']}\n{quote['translation'][:100]}...", timeout=10)
                    except:
                        pass
                    time.sleep(60)
                time.sleep(30)
        thread = threading.Thread(target=check_time, daemon=True)
        thread.start()

if __name__ == '__main__':
    GitaApp().run()