from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from Video.models import Video
from Video.serializers import VideoSerializer
from .models import SearchQuery  
from django.core.paginator import Paginator

@api_view(['GET'])
def search_videos(request):
    query = request.GET.get('q', '')  # Get the search term
    if query:
        # Save the search query for analytics or tracking
        SearchQuery.objects.create(query=query)

        # Perform search on both title and description using the __icontains lookup for case-insensitive matching
        results = Video.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        
        # Serialize the result list
        serialized_results = VideoSerializer(results, many=True)
        return Response({'results': serialized_results.data})

    return Response({'results': []})  # Return empty list if no query

    


def browse_videos(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    videos = Video.objects.all()
    
    if query:
        videos = videos.filter(title__icontains=query) | videos.filter(description__icontains=query)
    
    if category:
        videos = videos.filter(category__iexact=category)

    print(f"Search query: {query}")
    print(f"Filtered video count: {videos.count()}")
    paginator = Paginator(videos, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'browse.html', {'page_obj': page_obj, 'query': query, 'category': category})    

