// src/components/DataSourceFooter.tsx
'use client';

import React from 'react';
import { ArrowUpRight } from 'lucide-react';

interface DataSourceItem {
  name: string;
  region: string;
  url: string;
}

const SEATTLE_DATA_SOURCES: DataSourceItem[] = [
  // 图书馆系统
  { name: '西雅图公共图书馆 (SPL)', region: '西雅图', url: 'https://www.spl.org' },
  { name: '金县图书馆系统 (KCLS)', region: '东区/全县', url: 'https://kcls.org' },
  { name: 'Sno-Isle 图书馆', region: '北区', url: 'https://www.sno-isle.org' },
  { name: 'Pierce County Library', region: '南区', url: 'https://www.mypcls.org' },

  // 科学探索与核心场馆
  { name: 'Pacific Science Center', region: '西雅图', url: 'https://pacificsciencecenter.org' },
  { name: 'KidsQuest 儿童博物馆', region: '东区', url: 'https://www.kidsquestmuseum.org' },
  { name: '飞行博物馆 (Museum of Flight)', region: '南区', url: 'https://www.museumofflight.org' },
  { name: '伯克自然历史博物馆 (Burke)', region: '西雅图', url: 'https://www.burkemuseum.org' },
  { name: 'MoPOP 流行文化博物馆', region: '西雅图', url: 'https://www.mopop.org' },
  { name: 'Imagine 儿童博物馆', region: '北区', url: 'https://www.imaginecm.org' },
  { name: 'Hands On 儿童博物馆', region: '南区', url: 'https://www.hocm.org' },
  { name: '西雅图儿童博物馆', region: '西雅图', url: 'https://thechildrensmuseum.org' },

  // 动物园、水族馆与农场
  { name: 'Woodland Park 动物园', region: '西雅图', url: 'https://www.zoo.org' },
  { name: '西雅图水族馆 (Seattle Aquarium)', region: '西雅图', url: 'https://www.seattleaquarium.org' },
  { name: 'Point Defiance 动物园水族馆', region: '南区', url: 'https://www.pdza.org' },
  { name: 'Farrel-McWhirter 农场公园', region: '东区', url: 'https://www.redmond.gov/parks' },
  { name: 'Cougar Mountain 动物园', region: '东区', url: 'https://www.cougarmountainzoo.org' },
  { name: '贝尔维尤植物园 (Bellevue Botanical)', region: '东区', url: 'https://bellevuebotanical.org' },

  // 公园管理与本地亲子日历
  { name: '西雅图公园与休闲局 (Seattle Parks)', region: '西雅图', url: 'https://www.seattle.gov/parks' },
  { name: '金县公园管理局 (King County Parks)', region: '全县', url: 'https://kingcounty.gov/parks' },
  { name: 'ParentMap 西雅图', region: '大都会区', url: 'https://www.parentmap.com' },
  { name: 'Seattle’s Child', region: '大都会区', url: 'https://www.seattleschild.com' },
  { name: 'Macaroni KID Eastside', region: '东区', url: 'https://cherryvalley.macaronikid.com' },
];

export default function DataSourceFooter() {
  return (
    <footer className="w-full bg-slate-50/70 border-t border-slate-200 px-6 py-4 text-xs text-slate-500">
      <div className="max-w-[1600px] mx-auto space-y-3">
        {/* 标题说明 */}
        <div className="flex items-center justify-between">
          <span className="font-semibold text-slate-700">活动来源</span>
          <span className="text-[11px] text-slate-400">持续更新</span>
        </div>

        {/* 外链矩阵流 */}
        <div className="flex flex-wrap gap-x-5 gap-y-2 leading-relaxed">
          {SEATTLE_DATA_SOURCES.map((source) => (
            <a
              key={source.name}
              href={source.url}
              target="_blank"
              rel="noopener noreferrer"
              className="group inline-flex items-center gap-1 hover:text-slate-900 transition-colors"
            >
              <span className="text-slate-700 group-hover:text-blue-600 transition-colors">
                {source.name}
              </span>
              <span className="text-[11px] text-slate-400 font-normal">
                {source.region}
              </span>
              <ArrowUpRight className="w-3 h-3 text-slate-300 group-hover:text-slate-600 transition-colors" />
            </a>
          ))}
        </div>
      </div>
    </footer>
  );
}