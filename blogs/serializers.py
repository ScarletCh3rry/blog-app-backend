from django.db.models import Sum
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from blogs.models import PostItem, Tag, Blog, UserPostRelation, Comment, Subscription, Quiz, Question, Answer, \
    PassedQuestion
from users.models import CustomUser


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'name',
            'slug',
            'id',
        ]


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'login',
            'avatar',
        ]


class BlogSerializer(ModelSerializer):
    class Meta:
        model = Blog
        read_only_fields = ('slug',)
        fields = [
            'title',
            'owner',
            'description',
            'slug',
        ]

    owner = CustomUserSerializer(read_only=True)


class PostSerializer(ModelSerializer):

    class Meta:
        model = PostItem
        fields = [
            'title',
            'description',
            'tags',
            'creation_date',
            'likes_count',
            'comments_count',
            'quizzes_count',
            'views_count',
            'blog',
            'id',
            'is_liked',
            'slug',
            'image'
        ]
        read_only_fields = ['likes_count', 'comments_count', 'quizzes_count', 'views_count']

    likes_count = SerializerMethodField()
    views_count = SerializerMethodField()
    comments_count = SerializerMethodField()
    quizzes_count = SerializerMethodField()
    is_liked = SerializerMethodField()

    def get_likes_count(self, instance: PostItem):
        return UserPostRelation.objects.filter(post=instance, like=True).count()

    def get_views_count(self, instance: PostItem):
        return UserPostRelation.objects.filter(post=instance, watched=True).count()

    def get_comments_count(self, instance: PostItem):
        return Comment.objects.filter(post=instance).count()

    def get_quizzes_count(self, instance: PostItem):
        return Quiz.objects.filter(post=instance).count()

    def get_is_liked(self, instance: PostItem):
        if not self.context['request'].user.is_authenticated:
            return False
        return UserPostRelation.objects.filter(post=instance, like=True, user=self.context['request'].user).exists()

    blog = BlogSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)


class FullBlogSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            'title',
            'owner',
            'description',
            'slug',
            'id'
        ]

    owner = CustomUserSerializer(read_only=True)


class PostLikeSerializer(ModelSerializer):
    class Meta:
        model = UserPostRelation
        fields = [
            'like',
            'watched'
        ]


class PostCommentSerializer(ModelSerializer):
    class Meta:
        read_only_fields = ['owner']
        model = Comment
        fields = [
            'text',
            'owner',
            'post',
            'id'
        ]

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data['owner'] = CustomUserSerializer(CustomUser.objects.get(id=data['owner'])).data
    #     return data

    def create(self, validated_data):
        return super().create(dict(**validated_data, owner=self.context['request'].user))

    owner = CustomUserSerializer(read_only=True)


class CreatePostSerializer(ModelSerializer):
    blog = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Blog.objects.all()
    )

    class Meta:
        read_only_fields = ['slug']
        model = PostItem
        fields = [
            'title',
            'description',
            'tags',
            'blog',
            'slug',
            'image'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tags'] = TagSerializer(Tag.objects.filter(id__in=representation['tags']), many=True).data
        representation['blog'] = BlogSerializer(Blog.objects.get(slug=representation['blog'])).data
        return representation

    def validate(self, attrs):
        # if not self.context['request'].user.blogs.filter(slug=attrs['blog']).exists():
        if not attrs['blog'].owner == self.context['request'].user:
            raise serializers.ValidationError({'blog': 'Нельзя создавать посты для чужих блогов'})
        return super().validate(attrs)


class EditPostSerializer(ModelSerializer):
    class Meta:
        model = PostItem
        fields = [
            'image'
        ]



class CreateBlogSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            'title',
            'owner',
            'description',
            'slug',
        ]
        read_only_fields = ['owner', 'slug']

    owner = CustomUserSerializer(read_only=True)

    def save(self, **kwargs):
        return super().save(**kwargs, owner=self.context['request'].user)


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = [
            'subscription',
        ]


class SubscriptionStatusSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = [
            'subscription_status'
        ]


class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'answer',
            'was_chosen_count',
            'id'
        ]

    was_chosen_count = SerializerMethodField()

    def get_was_chosen_count(self, instance: Answer):
        return instance.passed_questions.count()


class PassedQuestionSerializer(ModelSerializer):
    class Meta:
        model = PassedQuestion
        fields = [
            'answer',
            'user'
        ]

    answer = AnswerSerializer()
    user = CustomUserSerializer()


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'question',
            'answers',
            'id',
            'chosen',
            'total_answers'
        ]

    chosen = SerializerMethodField()
    answers = AnswerSerializer(many=True)
    total_answers = SerializerMethodField()

    def get_total_answers(self, instance: Question):
        all_answers = instance.answers.all()
        all_passed_answers = PassedQuestion.objects.filter(answer__in=all_answers).all().count()
        return all_passed_answers

    def get_chosen(self, instance: Question):
        user: CustomUser = self.context['request'].user
        answer = instance.answers.filter(passed_questions__user=user).first()
        if answer is None:
            return None
        return answer.answer


class QuizSerializer(ModelSerializer):
    class Meta:
        model = Quiz
        fields = [
            'questions',
            'title',
            'slug',
            'sub_answers_list',
            'post',
            'id'
        ]

    sub_answers_list = SerializerMethodField()
    questions = QuestionSerializer(read_only=True, many=True)

    def get_sub_answers_list(self, instance: Quiz):
        user: CustomUser = self.context['request'].user
        user_you_subscribed_to = user.subscriptions.filter(subscription_status=True).values_list(
            'user_you_subscribed_to',
            flat=True)
        answers = PassedQuestion.objects.filter(user__in=user_you_subscribed_to, answer__question__quiz=instance)
        return PassedQuestionSerializer(answers, many=True).data


class CreateQuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'question',
            'answers',
            'quiz'
        ]

    quiz = serializers.SlugField()
    answers = serializers.ListField(
        child=serializers.CharField(max_length=70)
    )

    def create(self, validated_data):
        quiz = Quiz.objects.get(slug=validated_data['quiz'])
        question = Question.objects.create(question=validated_data['question'], quiz=quiz)
        for answer in validated_data['answers']:
            Answer.objects.create(answer=answer, question=question)
        return question

    def to_representation(self, instance):
        return dict()
