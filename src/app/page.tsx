// src/app/page.tsx
'use client';

import React, { useState, useEffect, useMemo } from 'react';
import dynamic from 'next/dynamic';
import FilterBar, { FilterState } from '@/components/FilterBar';
import EventList from '@/components/EventList';
import { WeekendEventFeature, WeekendEventGeoJSON } from '@/types/event';
import DataSourceFooter from '@/components/DataSourceFooter';

// 动态载入 Leaflet 组件，禁用 SSR
const LeafletMap = dynamic(() => import('@/components/LeafletMap'), {
  ssr: false,
  loading: () => (
    <div className="h-full w-full bg-slate-100 flex items-center justify-center text-xs text-slate-400">
      地图加载中...
    </div>
  ),
});

const INITIAL_FILTERS: FilterState = {
  datePreset: 'month_and_next',
  searchQuery: '',
  regions: ['seattle', 'eastside', 'north', 'south'],
  ageBuckets: ['preschool', 'elementary'],
  timeSlots: ['morning', 'afternoon'],
  isFreeOnly: false,
  isIndoorOnly: false,
  category: 'all',
};

export default function WeekendPage() {
  const [filters, setFilters] = useState<FilterState>(INITIAL_FILTERS);
  const [allEvents, setAllEvents] = useState<WeekendEventFeature[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);

  // 从本地 public 目录加载种子数据
  useEffect(() => {
    fetch('/data/events.geojson')
      .then((res) => res.json())
      .then((data: WeekendEventGeoJSON) => {
        setAllEvents(data.features || []);
      })
      .catch((err) => console.error('Failed to load events:', err));
  }, []);

  // 纯客户端多条件复合筛选
  const filteredEvents = useMemo(() => {
    return allEvents.filter((item) => {
      const p = item.properties;

      // 关键词搜索
      if (filters.searchQuery.trim()) {
        const q = filters.searchQuery.toLowerCase();
        const matchTitle = p.title.toLowerCase().includes(q);
        const matchVenue = p.location.venueName.toLowerCase().includes(q);
        const matchCity = p.location.city.toLowerCase().includes(q);
        if (!matchTitle && !matchVenue && !matchCity) return false;
      }

      // 区域筛选
      if (!filters.regions.includes(p.location.region)) return false;

      // 年龄段
      const matchAge = filters.ageBuckets.some((b) =>
        p.familyAttributes.ageBuckets.includes(b)
      );
      if (!matchAge) return false;

      // 时段
      if (p.schedule.timeSlot && !filters.timeSlots.includes(p.schedule.timeSlot)) {
        return false;
      }

      // 免费开关
      if (filters.isFreeOnly && !p.familyAttributes.isFree) return false;

      // 室内避雨开关
      if (filters.isIndoorOnly && p.familyAttributes.environment !== 'indoor') {
        return false;
      }

      // 4大分类胶囊
      if (filters.category !== 'all' && p.category !== filters.category) {
        return false;
      }

      return true;
    });
  }, [allEvents, filters]);

  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden bg-white text-slate-800">
      {/* 顶栏控制台 */}
      <FilterBar filters={filters} onChange={setFilters} />

      {/* 下方分栏主体 */}
      <main className="flex flex-1 overflow-hidden">
        {/* 左侧可滚动活动列表 */}
        <section className="w-full md:w-[460px] lg:w-[500px] h-full shrink-0 border-r border-slate-200">
          <EventList
            events={filteredEvents}
            selectedId={selectedId}
            onSelectEvent={setSelectedId}
            onClearFilters={() => setFilters(INITIAL_FILTERS)}
          />
        </section>

        {/* 右侧交互式地图 */}
        <section className="flex-1 h-full hidden md:block">
          <LeafletMap
            events={filteredEvents}
            selectedId={selectedId}
            onSelectEvent={setSelectedId}
          />
        </section>
      </main>

      {/* 底部数据源栏 */}
      <DataSourceFooter />
    </div>
  );
}