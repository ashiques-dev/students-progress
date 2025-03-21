from django.core.files.storage import default_storage
from school.models import School


def update_or_create_school(request, school=None):
    name = request.POST.get('name')
    state = request.POST.get('state')
    district = request.POST.get('district')
    place = request.POST.get('place')
    school_picture = request.FILES.get('school_picture')
    description = request.POST.get('description')

    if school:
        school.name = name
        school.district = district
        school.state = state
        school.place = place
        school.description = description
        school.updated_by = request.user

        if school_picture:
            if school.school_picture:
                old_file_path = school.school_picture.path
                if default_storage.exists(old_file_path):
                    default_storage.delete(old_file_path)
            school.school_picture = school_picture

        school.save()

        return {
            'name': school.name,
            'place': f'{school.place or "Unknown"}, {school.district or "Unknown"}, {school.state or "Unknown"}',
            'description': school.description or "Not provided"
        }
    else:
        new_school = School(
            name=name,
            state=state,
            district=district,
            place=place,
            school_picture=school_picture,
            description=description,
            updated_by=request.user
        )

        new_school.save()
        return {
            'id': new_school.id,
            'name': new_school.name,
            'place': new_school.place,
        }
