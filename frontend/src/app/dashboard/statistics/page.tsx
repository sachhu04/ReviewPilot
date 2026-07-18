"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { FileCode, Star, AlertTriangle, CheckCircle2 } from "lucide-react";
import { ReviewTrendChart } from "@/components/dashboard/ReviewTrendChart";

type Statistics = {
  total_reviews: number;
  average_score: number;
  critical_issues: number;
  merge_ready_percentage: number;
};

export default function StatisticsPage() {
  const [stats, setStats] = useState<Statistics | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // In a real app, fetch from /api/v1/review/statistics
    setTimeout(() => {
      setStats({
        total_reviews: 1248,
        average_score: 8.6,
        critical_issues: 12,
        merge_ready_percentage: 78
      });
      setIsLoading(false);
    }, 600);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Statistics</h2>
        <p className="text-muted-foreground mt-2">
          Deep dive into your code review metrics and team performance.
        </p>
      </div>

      {isLoading || !stats ? (
        <div className="h-64 flex items-center justify-center text-muted-foreground">
          Loading statistics...
        </div>
      ) : (
        <div className="space-y-8">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Reviews</CardTitle>
                <FileCode className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.total_reviews}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Average Score</CardTitle>
                <Star className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.average_score}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Critical Issues</CardTitle>
                <AlertTriangle className="h-4 w-4 text-destructive" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.critical_issues}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Merge Ready %</CardTitle>
                <CheckCircle2 className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.merge_ready_percentage}%</div>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Historical Trend</CardTitle>
              <CardDescription>Number of reviews performed over the last 6 months.</CardDescription>
            </CardHeader>
            <CardContent className="pl-2">
              <ReviewTrendChart />
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
