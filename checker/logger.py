import pusher

channels_client = pusher.Pusher(
    app_id='874627',
    key='161193c85aa3be59e44d',
    secret='c4006e13b614fe1f129a',
    cluster='ap1',
    ssl=True
)


def info(message):
    channels_client.trigger('my-channel', 'my-event', {'message': message})
