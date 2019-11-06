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
#This is to get Template for Search vehicles
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import HttpResponse
from rest_framework.views import APIView
from django.contrib.auth.models import User
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
        qs=Contest.objects.filter().order_by("-created_at")
        return qs

    # This function is used to manually change the columns
    def render_column(self, row, column):
        # We want to render filename as a custom column
        if column == 'contest_name':
            return (row.contest_name).upper()
        elif column == 'entrydate':
            return '%s' % row.intime.isoformat()# .strftime('%Y-%m-%d %H:%M:%S')
        elif column == 'action':
            return '<a href="#" class="participate"  data-id="' + str(row.id) + '/participate/"><i class="icon-pencil"></i>Participate</a>'
        else:
            return super(ContestList, self).render_column(row, column)


    # def filter_queryset(self, qs):
    #     # print("Query Set",qs)
    #     search = self.request.GET.get(u'search[value]', None)
    #     print("Search", search)
    #     if search:
    #         if (search.lower() == "valid"):
    #             valid_search = True
    #             qs = qs.filter(
    #                 Q(brand__icontains=search) | Q(color__icontains=search) | Q(client_name__icontains=search) | Q(
    #                     plate_no__icontains=search) | Q(m_type__icontains=search) | Q(
    #                     vehical_type__icontains=search) | Q(valid=valid_search))
    #         elif(search.lower() == "invalid"):
    #             valid_search = False
    #             qs = qs.filter(
    #                 Q(brand__icontains=search) | Q(color__icontains=search) | Q(client_name__icontains=search) | Q(
    #                     plate_no__icontains=search) | Q(m_type__icontains=search) | Q(
    #                     vehical_type__icontains=search) | Q(valid=valid_search))
    #         else:
    #             qs = qs.filter(
    #                 Q(brand__icontains=search) | Q(color__icontains=search) | Q(client_name__icontains=search) | Q(
    #                     plate_no__icontains=search) | Q(m_type__icontains=search) | Q(
    #                     vehical_type__icontains=search))
    #
    #         print("Query Set 0", qs)
    #
    #     select_search_client_name = self.request.GET.get('columns[1][search][value]')
    #     print("select_search_client_name Search", select_search_client_name)
    #     if select_search_client_name:
    #         qs = qs.filter(Q(client_name__icontains=select_search_client_name))
    #         print("Query Set 1", qs)
    #
    #     select_search_vehicle = self.request.GET.get('columns[7][search][value]')
    #     print("select_search_vehicle Search", select_search_vehicle)
    #     if select_search_vehicle:
    #         qs = qs.filter(Q(plate_no__icontains=select_search_vehicle))
    #         print("Query Set 6", qs)
    #
    #     select_search_brand = self.request.GET.get('columns[8][search][value]')
    #     print("select_search_brand Search", select_search_brand)
    #     if(select_search_brand == "UNKNOWN"):
    #         select_search_brand = "Not Found"
    #     print("select_search_brand Search UNKNOWN", select_search_brand)
    #     if select_search_brand:
    #         qs = qs.filter(Q(brand__icontains=select_search_brand))
    #         print("Query Set 7", qs)
    #
    #     select_search_color = self.request.GET.get('columns[9][search][value]')
    #     print("select_search_color Search", select_search_color)
    #     if select_search_color:
    #         qs = qs.filter(Q(color__icontains=select_search_color))
    #         print("Query Set 8", qs)
    #
    #     select_search_vehicle_type = self.request.GET.get('columns[12][search][value]')
    #     print("select_search_vehicle_type Search", select_search_vehicle_type)
    #     if select_search_vehicle_type:
    #         qs = qs.filter(Q(vehical_type__icontains=select_search_vehicle_type))
    #         print("Query Set 11", qs)
    #
    #     select_search_member_type = self.request.GET.get('columns[13][search][value]')
    #     print("select_search_member_type Search", select_search_member_type)
    #     if select_search_member_type:
    #         qs = qs.filter(Q(m_type__icontains=select_search_member_type))
    #         print("Query Set 12", qs)
    #
    #     select_search_valid = self.request.GET.get('columns[14][search][value]')
    #     print("select_search_valid Search", select_search_valid)
    #     if select_search_valid:
    #         if select_search_valid.lower() == "valid":
    #             valid_search = True
    #         else:
    #             valid_search = False
    #         qs = qs.filter(Q(valid=valid_search))
    #         print("Query Set 12", qs)
    #
    #     return qs

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
            message = "Your have already Voted for {}".format(contestobject.contest_name)
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
            message = "Your Vote is Submitted for {}".format(contestobject)
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
        self.model = Participants()
        self.model.participant_user = user_object
        self.model.participant_contest = contest_object
        self.model.photo = self.request.FILES['photo']
        self.model.save()
        print("Participate Model Saved")
        messages.success(self.request, f'You have successfully participated in contest '+str(contest_object.id))
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
