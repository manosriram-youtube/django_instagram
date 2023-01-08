from rest_framework import serializers
from app.models import Post, PostComment, PostLike, User, UserFollow

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
    bio = serializers.CharField()

    def create(self, validated_data):
        return User.objects.create(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    title = serializers.CharField()
    description = serializers.CharField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def update(self, instance, validated_data):
        print(validated_data)
        if instance.user.id == validated_data["user"].id:
            return super().update(instance, validated_data)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = "__all__"


    comment_text = serializers.CharField(max_length=264)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    def save(self, **kwargs):
        print(kwargs)
        self.post = kwargs["post"]
        return super().save(**kwargs)

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = "__all__"

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

class UserFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollow
        fields = "__all__"

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    follows_id = serializers.PrimaryKeyRelatedField(read_only=True)
