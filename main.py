import pyglet
from dataclasses import dataclass

m_per_px = 0.5
g = 9.81 / m_per_px

@dataclass
class Ball:
    position : list[int]

    from_hand : int = 0
    to_hand : int = 0

    started : int = 0
    arrive : int = 0

    shape : pyglet.shapes.ShapeBase = pyglet.shapes.Circle(0, 0, 1)

class GraphicsEngine:
    def __init__(self):
        self.window = pyglet.window.Window() 
        self.batch = pyglet.graphics.Batch()
        pyglet.gl.glClearColor(0.8, 0.8, 0.8, 1.0)

        self.hands_positions = [(250, 100), (600, 100)]

        self.window.on_draw = self.on_draw
    
        self.left_hand = pyglet.shapes.Rectangle(self.hands_positions[0][0], self.hands_positions[0][1], 20, 10, color=(55, 55, 255), batch=self.batch)
        self.right_hand = pyglet.shapes.Rectangle(self.hands_positions[1][0], self.hands_positions[0][1], 20, 10, color=(55, 55, 255), batch=self.batch)

        self.balls = []

    def on_draw(self):
        self.window.clear()
        self.batch.draw()

    def update_balls(self, balls):
        if len(balls) > len(self.balls):
            for b in range(len(self.balls), len(balls)):
                self.balls.append(pyglet.shapes.Circle(0, 0, 10, color=(255, 0, 0, 255), batch=self.batch))

        for i, b in enumerate(balls):
            self.balls[i].x = b.position[0]
            self.balls[i].y = b.position[1]

    def reset(self):
        balls.clear()

class Engine:
    def __init__(self, graphics):
        self.in_left = []
        self.in_right = []
        self.in_the_air = []

        self.previous_time : float = -1
        self.passed_time : float = 0

        self.hands_positions = [(250, 100), (650, 100)]
        self.graphics = graphics

        self.balls = []
        
        self.sequence = [3]
        self.started : bool = False
    
    def set_text_sequence(self, text_sequence : str):
        self.sequence = self.parse_sequence(text_sequence)

    def start(self):
        pyglet.clock.schedule_interval(self.update, 0.1)
        pyglet.app.run()

    def parse_sequence(self, sequence : str):
        return list(map(int, sequence))

    def check_sequence(self, sequence : list) -> bool:
        if not is_integer(sum(sequence)/len(sequence)):
            return False

    def reset(self):
        self.previous_time : float = -1
        self.passed_time : float = 0

    def update(self, dt):
        self.passed_time += dt
        current_beat = int(self.passed_time)

        balls_to_remove = []
        for b in self.in_the_air:
            ball = self.balls[b]
            if ball.arrive == current_beat :
                balls_to_remove.append(b)
                if ball.to_hand == 0:
                    self.in_left.append(b)
                else :
                    self.in_right.append(b)
            
                continue
            
            #Move the ball
            d_time =  (self.passed_time - ball.started)
            ball.position[0] = self.hands_positions[ball.from_hand][0] + d_time*(self.hands_positions[ball.to_hand][0] - self.hands_positions[ball.from_hand][0]) / (ball.arrive - ball.started)
            ball.position[1] = self.hands_positions[ball.from_hand][1] -2*g*(d_time)*(self.passed_time - ball.arrive)
            ball.shape.x = ball.position[0]
            ball.shape.y = ball.position[1]

        for b in balls_to_remove:
            self.in_the_air.remove(b)

        self.graphics.update_balls(self.balls)

        #Launch new balls
        if current_beat == int(self.previous_time):
            return 

        sequence_position = current_beat % len(self.sequence)
        sequence_value = self.sequence[sequence_position]

        if sequence_value == 0:
            return

        current_ball = None
        if current_beat % 2 == 0: #throw from the left hand
            if len(self.in_left) > 0:
                current_ball = self.in_left.pop()
            else:
                self.balls.append(Ball([0,0], 0, 0, 0))
                current_ball = len(self.balls) - 1
        else :
            if len(self.in_right) > 0:
                current_ball = self.in_right.pop()
            else:
                self.balls.append(Ball([0,0], 0, 0, 0))
                current_ball = len(self.balls) - 1

        self.balls[current_ball].from_hand = current_beat % 2

        if sequence_value % 2 == 0: 
            self.balls[current_ball].to_hand = self.balls[current_ball].from_hand
        else :
            self.balls[current_ball].to_hand = (self.balls[current_ball].from_hand + 1) % 2  

        self.in_the_air.append(current_ball)
        self.balls[current_ball].started=current_beat
        self.balls[current_ball].arrive=current_beat + sequence_value

        self.previous_time = self.passed_time


if __name__ == "__main__":
    graphics = GraphicsEngine()
    engine = Engine(graphics=graphics)
    engine.set_text_sequence("531531441423423")
    engine.start()