extends Node2D

const CENTER = Vector2(640,360)

func _on_goal_left_body_entered(body):
	reset()


func _on_goal_right_body_entered(body):
	reset()

func reset():
	$Ball.position = CENTER
	$Ball.call("set_ball_velocity")
	$Player.position.y = CENTER.y
	$Enemy.position.y = CENTER.y

