"use client";

import { useGetV2ListLibraryAgentsInfinite } from "@/app/api/__generated__/endpoints/library/library";
import { LibraryAgentResponse } from "@/app/api/__generated__/models/libraryAgentResponse";
import { useLibraryPageContext } from "../state-provider";

export const useLibraryAgentList = () => {
  const { searchTerm, librarySort } = useLibraryPageContext();
  const {
    data: agents,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading: agentLoading,
  } = useGetV2ListLibraryAgentsInfinite(
    {
      page: 1,
      page_size: 8,
      search_term: searchTerm || undefined,
      sort_by: librarySort,
    },
    {
      query: {
        getNextPageParam: (lastPage) => {
          // Only paginate on successful responses with valid pagination data
          if (!lastPage || lastPage.status !== 200 || !lastPage.data) {
            return undefined;
          }

          const response = lastPage.data as LibraryAgentResponse;
          const pagination = response.pagination;
          
          if (!pagination || typeof pagination.current_page !== 'number') {
            return undefined;
          }

          const isMore =
            pagination.current_page * pagination.page_size <
            pagination.total_items;

          return isMore ? pagination.current_page + 1 : undefined;
        },
      },
    },
  );

  const allAgents =
    agents?.pages?.flatMap((page) => {
      // Only process successful responses with valid data
      if (!page || page.status !== 200 || !page.data) return [];
      
      const response = page.data as LibraryAgentResponse;
      return response?.agents || [];
    }) ?? [];

  const agentCount = (() => {
    const firstPage = agents?.pages?.[0];
    // Only count from successful responses
    if (!firstPage || firstPage.status !== 200 || !firstPage.data) return 0;
    
    const response = firstPage.data as LibraryAgentResponse;
    return response?.pagination?.total_items || 0;
  })();

  return {
    allAgents,
    agentLoading,
    hasNextPage,
    agentCount,
    isFetchingNextPage,
    fetchNextPage,
  };
};
