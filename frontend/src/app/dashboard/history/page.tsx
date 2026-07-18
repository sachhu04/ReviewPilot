"use client";

import { useEffect, useState } from "react";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ArrowRight, FileCode } from "lucide-react";
import Link from "next/link";

type ReviewHistory = {
  id: number;
  filename: string;
  status: string;
  score: number;
  created_at: string;
  language: string;
};

export default function HistoryPage() {
  const [history, setHistory] = useState<ReviewHistory[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // In a real app, we'd fetch from /api/v1/review/history
    // Simulating API call for the UI prototype
    setTimeout(() => {
      setHistory([
        { id: 104, filename: "auth_controller.py", status: "Completed", score: 8.2, created_at: "2026-07-18T10:00:00Z", language: "python" },
        { id: 103, filename: "Dashboard.tsx", status: "Completed", score: 9.1, created_at: "2026-07-17T15:30:00Z", language: "typescript" },
        { id: 102, filename: "main.cpp", status: "Completed", score: 6.5, created_at: "2026-07-16T09:15:00Z", language: "cpp" },
        { id: 101, filename: "db_utils.go", status: "Failed", score: 0.0, created_at: "2026-07-15T14:20:00Z", language: "go" },
      ]);
      setIsLoading(false);
    }, 800);
  }, []);

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "Completed": return <Badge className="bg-emerald-500/10 text-emerald-500 hover:bg-emerald-500/20 border-emerald-500/20">Completed</Badge>;
      case "Processing": return <Badge className="bg-blue-500/10 text-blue-500 hover:bg-blue-500/20 border-blue-500/20">Processing</Badge>;
      case "Failed": return <Badge variant="destructive">Failed</Badge>;
      default: return <Badge variant="secondary">{status}</Badge>;
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 8.5) return "text-emerald-500";
    if (score >= 7.0) return "text-amber-500";
    return "text-destructive";
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Review History</h2>
        <p className="text-muted-foreground mt-2">
          View all your previous code reviews and their outcomes.
        </p>
      </div>

      <div className="rounded-md border bg-card/50">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>File / PR</TableHead>
              <TableHead>Language</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Score</TableHead>
              <TableHead>Date</TableHead>
              <TableHead className="text-right">Action</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              <TableRow>
                <TableCell colSpan={6} className="h-24 text-center text-muted-foreground">
                  Loading history...
                </TableCell>
              </TableRow>
            ) : history.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} className="h-24 text-center text-muted-foreground">
                  No reviews found.
                </TableCell>
              </TableRow>
            ) : (
              history.map((item) => (
                <TableRow key={item.id}>
                  <TableCell className="font-medium">
                    <div className="flex items-center gap-2">
                      <FileCode className="h-4 w-4 text-muted-foreground" />
                      {item.filename}
                    </div>
                  </TableCell>
                  <TableCell className="capitalize">{item.language}</TableCell>
                  <TableCell>{getStatusBadge(item.status)}</TableCell>
                  <TableCell>
                    {item.status === "Completed" ? (
                      <span className={`font-semibold ${getScoreColor(item.score)}`}>
                        {item.score.toFixed(1)}
                      </span>
                    ) : (
                      <span className="text-muted-foreground">-</span>
                    )}
                  </TableCell>
                  <TableCell className="text-muted-foreground">
                    {new Date(item.created_at).toLocaleDateString()}
                  </TableCell>
                  <TableCell className="text-right">
                    <Button variant="ghost" size="sm" asChild disabled={item.status !== "Completed"}>
                      <Link href={`/dashboard/review/${item.id}`}>
                        View <ArrowRight className="ml-2 h-4 w-4" />
                      </Link>
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
