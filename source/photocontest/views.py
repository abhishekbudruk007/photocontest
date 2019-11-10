from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from braces.views import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Contest ,Participants ,Likes,Winner
from django_datatables_view.base_datatable_view import BaseDatatableView
from .serializers import ContestSerializer,ParticipantsSerializer,WinnerSerializer
from datetime import datetime
from django.views import generic
from .forms import ParticipantForm
from django.urls import reverse_lazy
from bootstrap_modal_forms.mixins import PassRequestMixin, DeleteMessageMixin
from django.urls import reverse
from rest_framework import generics
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import HttpResponse
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.db.models import Q
import json
class ContestTemplate(generic.TemplateView):
    template_name = "photocontest/contest_list.html"

class ContestList(BaseDatatableView):
    model = Contest
    serializer_class= ContestSerializer

    #Columns to be displayed in datatable
    columns = ['contest_name','contest_lastdate','action']
    order_columns = ['contest_name','contest_lastdate']

    def get_initial_queryset(self):
        #This query ( Select 8 from Contest order-by created_at DESC;)
        qs=Contest.objects.filter(contest_lastdate__gt=datetime.now()).order_by("-created_at")
        return qs

    # This function is used to manually change the columns
    def render_column(self, row, column):
        # We want to render filename as a custom column
        if column == 'contest_name':
            return (row.contest_name).upper()
        elif column == 'contest_lastdate':
            return '%s' % row.contest_lastdate.isoformat()# .strftime('%Y-%m-%d %H:%M:%S')
        elif column == 'action':
            return '<a href="#" class="participate"  data-id="' + str(row.id) + '/participate/"><i class="icon-pencil"></i>Participate</a>'
        else:
            return super(ContestList, self).render_column(row, column)


    def filter_queryset(self, qs):
        # print("Query Set",qs)
        search = self.request.GET.get(u'search[value]', None)
        print("Search", search)
        if search:
            qs = qs.filter(Q(contest_name__icontains=search))
            print("Query Set filter 0", qs)
        return qs

class LikeApi(APIView):

    def post(self,request):
        userid = request.POST.get('userid')
        contestid = request.POST.get('contestid')
        participatedid = request.POST.get('participatedid')
        print("Userid",userid)
        userobject = User.objects.filter(id=userid)[0]
        print("contestid",contestid)
        contestobject = Contest.objects.filter(id=contestid)[0]
        print("participatedid",participatedid)
        participateobject = Participants.objects.filter(id=participatedid)[0]

        if Likes.objects.filter(participant_id_id=participatedid, participant_contest_id=contestid,participant_user__in=userid).exists():
            message = "Your have already Voted for {0} {1}".format(participateobject.participant_user.first_name,participateobject.participant_user.last_name)
            return HttpResponse(json.dumps({"status": "failed", "message": message}), content_type="application/json")
        else:
            if Likes.objects.filter(participant_id_id=participatedid,participant_contest_id=contestid).exists():
                print("Exists")
                likes = Likes.objects.filter(participant_id_id=participatedid,participant_contest_id=contestid)[0]
                likes.participant_user.add(userobject)
            else:
                print("Does Not Exists")
                obj = Likes.objects.create(participant_id=participateobject,participant_contest=contestobject)
                obj.participant_user.add(userobject)
            message = "Your Vote is Submitted for {0} {1}".format(participateobject.participant_user.first_name,participateobject.participant_user.last_name)
            return HttpResponse(json.dumps({"status":"success","message":message}), content_type="application/json")

class Participate(LoginRequiredMixin,PassRequestMixin, SuccessMessageMixin,generic.CreateView):
    model = Participants
    form_class = ParticipantForm
    template_name = "photocontest/participate.html"
    success_message = 'You have successfully participated in this Contest'
    success_url = reverse_lazy('photocontest:contest_template')

    def form_valid(self, form):
        print("valid")
        user_object = self.request.user
        contest_object = Contest.objects.filter(id__iexact=self.kwargs["pk"])[0]
        print("contest_object",contest_object)
        already_exists = Participants.objects.filter(participant_user=user_object,participant_contest=contest_object)
        print("Already Exists")
        if(len(already_exists)>0):
            messages.error(self.request, f'You have already participated earlier in the contest '+str(contest_object.contest_name))
        else:
            self.model = Participants()
            self.model.participant_user = user_object
            self.model.participant_contest = contest_object
            self.model.photo = self.request.FILES['photo']
            self.model.save()
            print("Participate Model Saved")
            messages.success(self.request, f'You have successfully participated in the contest '+str(contest_object.contest_name))
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        print("invalid")
        print("Participate User Errors", form.errors)
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.

        Args:
            form: Assignment Form
            vehical_information_form: Assignment Question Form
        """
        return self.render_to_response(
            self.get_context_data(form=form,)
        )

    def get_success_url(self):
        return reverse('photocontest:contest_template')
