"use client";

import { useState } from "react";
import { UploadCloud, Code, GitPullRequest, ArrowRight, CheckCircle2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Progress } from "@/components/ui/progress";
import { useRouter } from "next/navigation";

const languages = [
  "C++", "Python", "Java", "JavaScript", "TypeScript", "Go", "Rust", "C#"
];

const pipelineSteps = [
  "Parsing Diff",
  "Running Static Analysis",
  "Building Prompt",
  "Calling Groq API",
  "AI Reviewing",
  "Formatting Report"
];

export default function NewReviewPage() {
  const router = useRouter();
  const [language, setLanguage] = useState<string>("");
  const [activeTab, setActiveTab] = useState<string>("upload");
  const [file, setFile] = useState<File | null>(null);
  const [pastedCode, setPastedCode] = useState<string>("");
  const [githubUrl, setGithubUrl] = useState<string>("");
  const [isReviewing, setIsReviewing] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);

  const handleReview = async () => {
    setIsReviewing(true);
    setCurrentStep(0);

    try {
      const formData = new FormData();
      formData.append("language", language);
      
      if (activeTab === "upload" && file) {
        formData.append("file", file);
      } else if (activeTab === "paste" && pastedCode) {
        formData.append("pasted_code", pastedCode);
      } else if (activeTab === "github" && githubUrl) {
        formData.append("github_url", githubUrl);
      }

      // Quick simulated UI progress while fetching
      const interval = setInterval(() => {
        setCurrentStep((prev) => (prev < pipelineSteps.length - 1 ? prev + 1 : prev));
      }, 1000);

      const res = await fetch("http://localhost:8000/api/v1/review/upload", {
        method: "POST",
        body: formData,
        headers: {
          "Authorization": "Bearer stub"
        }
      });
      
      const data = await res.json();
      clearInterval(interval);
      setCurrentStep(pipelineSteps.length);

      if (data.status === "success") {
        setTimeout(() => {
          setIsReviewing(false);
          router.push(`/dashboard`);
        }, 1000);
      } else {
        alert("Upload failed: " + data.detail);
        setIsReviewing(false);
      }
    } catch (e) {
      alert("Error connecting to backend");
      setIsReviewing(false);
    }
  };

  return (
    <div className="mx-auto max-w-4xl space-y-8">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">New Review</h2>
        <p className="text-muted-foreground mt-2">
          Submit code for AI-powered static analysis and architectural review.
        </p>
      </div>

      {!isReviewing ? (
        <Card className="border-border bg-card/50 shadow-sm">
          <CardHeader>
            <CardTitle>Source Code</CardTitle>
            <CardDescription>
              Select how you want to provide the code for review.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="upload" className="flex items-center gap-2">
                  <UploadCloud className="w-4 h-4" /> Upload File
                </TabsTrigger>
                <TabsTrigger value="paste" className="flex items-center gap-2">
                  <Code className="w-4 h-4" /> Paste Code
                </TabsTrigger>
                <TabsTrigger value="github" className="flex items-center gap-2">
                  <GitPullRequest className="w-4 h-4" /> GitHub PR
                </TabsTrigger>
              </TabsList>
              
              <div className="mt-6">
                <TabsContent value="upload">
                  <div className="flex justify-center items-center w-full">
                    <label htmlFor="dropzone-file" className="flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-lg cursor-pointer bg-muted/20 hover:bg-muted/50 border-border transition-colors">
                      <div className="flex flex-col items-center justify-center pt-5 pb-6 text-muted-foreground">
                        <UploadCloud className="w-10 h-10 mb-3" />
                        <p className="mb-2 text-sm font-semibold">Click to upload or drag and drop</p>
                        <p className="text-xs">Source code or diff files</p>
                        {file && <p className="mt-4 font-semibold text-primary">{file.name}</p>}
                      </div>
                      <input 
                        id="dropzone-file" 
                        type="file" 
                        className="hidden" 
                        onChange={(e) => setFile(e.target.files?.[0] || null)}
                      />
                    </label>
                  </div>
                </TabsContent>
                
                <TabsContent value="paste">
                  <div className="space-y-2">
                    <Label htmlFor="code-input">Raw Code or Diff</Label>
                    <Textarea 
                      id="code-input"
                      placeholder="Paste your code or git diff here..." 
                      className="min-h-[250px] font-mono text-sm bg-muted/20"
                      value={pastedCode}
                      onChange={(e) => setPastedCode(e.target.value)}
                    />
                  </div>
                </TabsContent>
                
                <TabsContent value="github">
                  <div className="space-y-2">
                    <Label htmlFor="github-url">Pull Request URL</Label>
                    <Input 
                      id="github-url"
                      placeholder="https://github.com/owner/repo/pull/123" 
                      className="bg-muted/20"
                      value={githubUrl}
                      onChange={(e) => setGithubUrl(e.target.value)}
                    />
                  </div>
                </TabsContent>
              </div>
            </Tabs>

            <div className="space-y-2 pt-4 border-t">
              <Label>Programming Language</Label>
              <Select value={language} onValueChange={(val) => setLanguage(val || "")}>
                <SelectTrigger className="w-full md:w-[300px]">
                  <SelectValue placeholder="Select language for static analysis" />
                </SelectTrigger>
                <SelectContent>
                  {languages.map((lang) => (
                    <SelectItem key={lang} value={lang.toLowerCase()}>
                      {lang}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </CardContent>
          <CardFooter className="bg-muted/20 px-6 py-4 flex justify-end border-t">
            <Button onClick={handleReview} className="gap-2" disabled={!language}>
              Start AI Review <ArrowRight className="w-4 h-4" />
            </Button>
          </CardFooter>
        </Card>
      ) : (
        <Card className="border-border shadow-sm max-w-2xl mx-auto mt-12">
          <CardHeader className="text-center pb-2">
            <CardTitle className="text-2xl">Reviewing Code</CardTitle>
            <CardDescription>Please wait while ReviewPilot analyzes your changes.</CardDescription>
          </CardHeader>
          <CardContent className="pt-6 pb-8 px-10">
            <div className="space-y-8">
              <Progress value={(currentStep / pipelineSteps.length) * 100} className="h-2" />
              
              <div className="space-y-4 pl-4 border-l-2 border-muted">
                {pipelineSteps.map((step, index) => {
                  const isCompleted = index < currentStep;
                  const isCurrent = index === currentStep;
                  
                  return (
                    <div key={step} className="flex items-center gap-4 relative">
                      <div className={`absolute -left-[1.35rem] p-0.5 rounded-full bg-background border ${isCompleted ? 'border-primary text-primary' : isCurrent ? 'border-foreground text-foreground' : 'border-muted text-muted-foreground'}`}>
                        <CheckCircle2 className="w-4 h-4" />
                      </div>
                      <span className={`text-sm font-medium ${isCompleted ? 'text-muted-foreground' : isCurrent ? 'text-foreground animate-pulse' : 'text-muted-foreground/50'}`}>
                        {step}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
