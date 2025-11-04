import { db } from '@/lib/db';
import { videos, companies } from '@/lib/db/schema';
import { eq, desc } from 'drizzle-orm';
import { GoogleOneTap } from '@/components/auth/GoogleOneTap';
import Link from 'next/link';

// ISR: Revalidate every hour
export const revalidate = 3600;

export default async function HomePage() {
  // Fetch published videos with company data
  const latestVideos = await db
    .select({
      video: videos,
      company: companies,
    })
    .from(videos)
    .leftJoin(companies, eq(videos.companyId, companies.id))
    .where(eq(videos.status, 'published'))
    .orderBy(desc(videos.publishedAt))
    .limit(12);

  return (
    <>
      <GoogleOneTap />

      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-blue-950">
        {/* Header */}
        <header className="border-b border-slate-800 bg-slate-950/50 backdrop-blur-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-xl">E</span>
                </div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                  EarningLens
                </h1>
              </div>

              <nav className="flex items-center space-x-6">
                <Link href="/videos" className="text-slate-400 hover:text-white transition">
                  Videos
                </Link>
                <Link href="/companies" className="text-slate-400 hover:text-white transition">
                  Companies
                </Link>
                <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition">
                  Sign In
                </button>
              </nav>
            </div>
          </div>
        </header>

        {/* Hero Section */}
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center space-y-6">
            <h2 className="text-5xl md:text-6xl font-bold text-white">
              Earnings Calls,
              <br />
              <span className="bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 bg-clip-text text-transparent">
                Visually Enhanced
              </span>
            </h2>
            <p className="text-xl text-slate-400 max-w-2xl mx-auto">
              Transform boring earnings call audio into engaging visual summaries with charts, transcripts, and data-driven insights.
            </p>
            <div className="flex items-center justify-center space-x-4">
              <div className="text-center">
                <div className="text-3xl font-bold text-white">{latestVideos.length}+</div>
                <div className="text-sm text-slate-500">Videos</div>
              </div>
              <div className="w-px h-12 bg-slate-700" />
              <div className="text-center">
                <div className="text-3xl font-bold text-white">50+</div>
                <div className="text-sm text-slate-500">Companies</div>
              </div>
              <div className="w-px h-12 bg-slate-700" />
              <div className="text-center">
                <div className="text-3xl font-bold text-white">Q4 2024</div>
                <div className="text-sm text-slate-500">Latest</div>
              </div>
            </div>
          </div>
        </section>

        {/* Video Grid */}
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="mb-8">
            <h3 className="text-2xl font-bold text-white mb-2">Latest Earnings Calls</h3>
            <p className="text-slate-400">Watch visual summaries of recent earnings calls</p>
          </div>

          {latestVideos.length === 0 ? (
            <div className="text-center py-20">
              <div className="text-6xl mb-4">📊</div>
              <h3 className="text-2xl font-bold text-white mb-2">Coming Soon</h3>
              <p className="text-slate-400">
                We're generating amazing earnings call videos. Check back soon!
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {latestVideos.map(({ video, company }) => (
                <Link
                  key={video.id}
                  href={`/${company?.ticker.toLowerCase()}/${video.slug}`}
                  className="group"
                >
                  <div className="bg-slate-900/50 border border-slate-800 rounded-xl overflow-hidden hover:border-blue-500/50 transition-all hover:shadow-lg hover:shadow-blue-500/10">
                    {/* Thumbnail */}
                    <div className="relative aspect-video bg-gradient-to-br from-slate-800 to-slate-900">
                      {video.data.thumbnailUrl ? (
                        <img
                          src={video.data.thumbnailUrl}
                          alt={video.data.title}
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        <div className="flex items-center justify-center h-full">
                          <span className="text-4xl">
                            {company?.data.logoUrl ? '🏢' : '📊'}
                          </span>
                        </div>
                      )}
                      <div className="absolute top-2 left-2 px-2 py-1 bg-black/80 rounded text-xs text-white font-medium">
                        {video.quarter} {video.year}
                      </div>
                    </div>

                    {/* Content */}
                    <div className="p-4">
                      <div className="flex items-center space-x-2 mb-2">
                        <span className="text-sm font-bold text-blue-400">
                          {company?.ticker}
                        </span>
                        <span className="text-slate-600">•</span>
                        <span className="text-sm text-slate-500">
                          {company?.data.industry}
                        </span>
                      </div>
                      <h4 className="text-lg font-semibold text-white mb-2 group-hover:text-blue-400 transition line-clamp-2">
                        {video.data.title}
                      </h4>
                      <div className="flex items-center justify-between text-sm text-slate-500">
                        <span>
                          {video.data.analytics?.views || 0} views
                        </span>
                        {video.data.duration && (
                          <span>
                            {Math.floor(video.data.duration / 60)}:{String(video.data.duration % 60).padStart(2, '0')}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </section>

        {/* Footer */}
        <footer className="border-t border-slate-800 mt-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="text-center text-slate-500 text-sm">
              © 2024 EarningLens. Transform earnings calls into visual insights.
            </div>
          </div>
        </footer>
      </div>
    </>
  );
}
