// src/app/page.tsx
'use client';

import React, { useState, useEffect, useMemo, useCallback } from 'react';
import dynamic from 'next/dynamic';
import FilterBar, { FilterState } from '@/components/FilterBar';
import EventList from '@/components/EventList';
import { WeekendEventFeature, WeekendEventGeoJSON } from '@/types/event';
import DataSourceFooter from '@/components/DataSourceFooter';

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

  const [listWidth, setListWidth] = useState(480);
  const [isResizing, setIsResizing] = useState(false);

  const [clientDates, setClientDates] = useState<{
    todayStr: string;
    maxLimitStr: string;
    thisSatStr: string;
    thisSunStr: string;
    nextSatStr: string;
    nextSunStr: string;
  } | null>(null);

  const startResizing = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    setIsResizing(true);
  }, []);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isResizing) return;
      const newWidth = Math.max(340, Math.min(e.clientX - 24, 820));
      setListWidth(newWidth);
    };

    const handleMouseUp = () => {
      setIsResizing(false);
    };

    if (isResizing) {
      window.addEventListener('mousemove', handleMouseMove);
      window.addEventListener('mouseup', handleMouseUp);
      document.body.style.cursor = 'col-resize';
      document.body.style.userSelect = 'none';
    } else {
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
    }

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isResizing]);

  useEffect(() => {
    const now = new Date();
    const pad = (n: number) => String(n).padStart(2, '0');
    const toYMD = (d: Date) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;

    const todayStr = toYMD(now);
    const maxDate = new Date(now);
    maxDate.setDate(now.getDate() + 30);
    const maxLimitStr = toYMD(maxDate);

    const day = now.getDay();
    const daysUntilSat = (6 - day + 7) % 7;
    const thisSat = new Date(now);
    thisSat.setDate(now.getDate() + (daysUntilSat === 0 && day !== 6 ? 6 : daysUntilSat));
    const thisSun = new Date(thisSat);
    thisSun.setDate(thisSat.getDate() + 1);

    const nextSat = new Date(thisSat);
    nextSat.setDate(thisSat.getDate() + 7);
    const nextSun = new Date(nextSat);
    nextSun.setDate(nextSat.getDate() + 1);

    setClientDates({
      todayStr,
      maxLimitStr,
      thisSatStr: toYMD(thisSat),
      thisSunStr: toYMD(thisSun),
      nextSatStr: toYMD(nextSat),
      nextSunStr: toYMD(nextSun),
    });

    fetch('/data/events.geojson')
      .then((res) => res.json())
      .then((data: WeekendEventGeoJSON) => {
        setAllEvents(data.features || []);
      })
      .catch((err) => console.error('Failed to load events:', err));
  }, []);

  const filteredEvents = useMemo(() => {
    if (!clientDates) return allEvents;

    return allEvents.filter((item) => {
      const p = item.properties;
      const eventDate = p.schedule.startDate;

      if (filters.datePreset === 'month_and_next') {
        if (eventDate < clientDates.todayStr || eventDate > clientDates.maxLimitStr) return false;
      } else if (filters.datePreset === 'this_weekend') {
        if (eventDate !== clientDates.thisSatStr && eventDate !== clientDates.thisSunStr) return false;
      } else if (filters.datePreset === 'next_weekend') {
        if (eventDate !== clientDates.nextSatStr && eventDate !== clientDates.nextSunStr) return false;
      } else if (filters.datePreset === 'custom') {
        const start = filters.customStartDate || clientDates.todayStr;
        const end = filters.customEndDate || clientDates.maxLimitStr;
        if (eventDate < start || eventDate > end) return false;
      }

      if (filters.searchQuery.trim()) {
        const q = filters.searchQuery.toLowerCase();
        const matchTitle = p.title.toLowerCase().includes(q);
        const matchVenue = p.location.venueName.toLowerCase().includes(q);
        const matchCity = p.location.city.toLowerCase().includes(q);
        if (!matchTitle && !matchVenue && !matchCity) return false;
      }

      if (!filters.regions.includes(p.location.region)) return false;

      const matchAge = filters.ageBuckets.some((b) =>
        p.familyAttributes.ageBuckets.includes(b)
      );
      if (!matchAge) return false;

      if (p.schedule.timeSlot && !filters.timeSlots.includes(p.schedule.timeSlot)) {
        return false;
      }

      if (filters.isFreeOnly && !p.familyAttributes.isFree) return false;
      if (filters.isIndoorOnly && p.familyAttributes.environment !== 'indoor') return false;

      if (filters.category !== 'all' && p.category !== filters.category) return false;

      return true;
    });
  }, [allEvents, filters, clientDates]);

  return (
    // 全局背景改为浅灰底色，带来浮动卡片层次感
    <div className="flex flex-col min-h-screen w-full bg-[#f8f9fa] text-slate-800">
      
      {/* 顶部标题栏：纤细优雅排版，取消吸顶 */}
      <div className="w-full max-w-[1600px] mx-auto px-6 pt-8 pb-4 text-center">
        <h1 className="text-3xl md:text-[34px] font-semibold text-slate-800 tracking-[0.02em] leading-tight">
          西雅图亲子活动
        </h1>
        <p className="text-xs text-slate-400 mt-1.5 font-normal tracking-wide">
          seattle kids weekend
        </p>
      </div>

      {/* 筛选卡片区 */}
      <section className="w-full max-w-[1600px] mx-auto px-6 pb-4">
        <FilterBar filters={filters} onChange={setFilters} />
      </section>

      {/* 主体分栏工作台：由两个独立的悬浮圆角卡片组成 */}
      <main className="flex-1 w-full max-w-[1600px] mx-auto px-6 pb-6 flex gap-4 h-[calc(100vh-250px)] min-h-[580px]">
        {/* 左侧活动列表卡片 */}
        <section
          style={{ width: `${listWidth}px` }}
          className="w-full md:w-auto h-full shrink-0 bg-white rounded-2xl shadow-sm border border-slate-200/80 overflow-hidden"
        >
          <EventList
            events={filteredEvents}
            selectedId={selectedId}
            onSelectEvent={setSelectedId}
            onClearFilters={() => setFilters(INITIAL_FILTERS)}
          />
        </section>

        {/* 拖动分割条 */}
        <div
          onMouseDown={startResizing}
          className={`hidden md:flex items-center justify-center w-2 -mx-1 h-full cursor-col-resize z-20 group select-none transition-colors ${
            isResizing ? 'bg-blue-500/20 rounded-full' : 'hover:bg-slate-200/60 rounded-full'
          }`}
          title="按住左右拖动调整列表宽度"
        >
          <div
            className={`w-[3px] h-8 rounded-full transition-colors ${
              isResizing ? 'bg-blue-600' : 'bg-slate-300 group-hover:bg-slate-400'
            }`}
          />
        </div>

        {/* 右侧地图悬浮卡片 */}
        <section className="flex-1 h-full hidden md:block relative bg-white rounded-2xl shadow-sm border border-slate-200/80 overflow-hidden">
          <LeafletMap
            events={filteredEvents}
            selectedId={selectedId}
            onSelectEvent={setSelectedId}
          />
        </section>
      </main>

      {/* 底部数据源栏 */}
      <footer className="w-full shrink-0 border-t border-slate-200/60 bg-white">
        <DataSourceFooter />
      </footer>
    </div>
  );
}