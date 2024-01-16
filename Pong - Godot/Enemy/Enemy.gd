extends CharacterBody2D

var speed = 450
var ball

func _ready():
	ball = get_parent().get_node("Ball")
func _physics_process(delta):
	if ball.position.y > position.y:
		velocity.y = -1
	else:
		velocity.y = 1
	velocity *= speed
	move_and_collide(velocity * delta)
