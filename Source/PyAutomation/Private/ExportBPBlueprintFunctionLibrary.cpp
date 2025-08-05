// Fill out your copyright notice in the Description page of Project Settings.


#include "ExportBPBlueprintFunctionLibrary.h"

#include "Editor.h"
#include "MeshMergeModule.h"
#include "AssetRegistry/AssetRegistryModule.h"


void UExportBPBlueprintFunctionLibrary::MergeActorToStaticMesh(const FString& InBasePackageName,
                                                               const TArray<UPrimitiveComponent*>& ComponentsToMerge, TArray<UObject*>& AssetsRef)
{
	//确认模块是否加载成功
	const IMeshMergeUtilities& MeshUtilities = FModuleManager::Get().LoadModuleChecked<IMeshMergeModule>("MeshMergeUtilities").GetUtilities();
	FVector MergedActorLocation;
	FMeshMergingSettings InSettings;
	InSettings.bBakeVertexDataToMesh  = true;
	
	
	if (ComponentsToMerge.Num())
	{

		UWorld* World = ComponentsToMerge[0]->GetWorld();
		checkf(World != nullptr, TEXT("Invalid World retrieved from Mesh components"));
		const float ScreenAreaSize = TNumericLimits<float>::Max();

		// If the merge destination package already exists, it is possible that the mesh is already used in a scene somewhere, or its materials or even just its textures.
		// Static primitives uniform buffers could become invalid after the operation completes and lead to memory corruption. To avoid it, we force a global reregister.
		if (FindObject<UObject>(nullptr, *InBasePackageName))
		{
			FGlobalComponentReregisterContext GlobalReregister;
			MeshUtilities.MergeComponentsToStaticMesh(ComponentsToMerge, World, InSettings, nullptr, nullptr, InBasePackageName, AssetsRef, MergedActorLocation, ScreenAreaSize, true);
		}
		else
		{
			MeshUtilities.MergeComponentsToStaticMesh(ComponentsToMerge, World, InSettings, nullptr, nullptr, InBasePackageName, AssetsRef, MergedActorLocation, ScreenAreaSize, true);
		}
	}
	
	if (AssetsRef.Num())
	{
		FAssetRegistryModule& AssetRegistry = FModuleManager::Get().LoadModuleChecked<FAssetRegistryModule>("AssetRegistry");
		int32 AssetCount = AssetsRef.Num();
		for (int32 AssetIndex = 0; AssetIndex < AssetCount; AssetIndex++)
		{
			AssetRegistry.AssetCreated(AssetsRef[AssetIndex]);
			GEditor->BroadcastObjectReimported(AssetsRef[AssetIndex]);
		}
	
		//Also notify the content browser that the new assets exists
		//内容栏中选中该资产
		// FContentBrowserModule& ContentBrowserModule = FModuleManager::Get().LoadModuleChecked<FContentBrowserModule>("ContentBrowser");
		// ContentBrowserModule.Get().SyncBrowserToAssets(AssetsRef, true);

		//移除临时Actor
		//TempActor->Destroy();
	}
}

void UExportBPBlueprintFunctionLibrary::GetComponentsFromBlueprintAsset(const UBlueprint* Blueprint,
	TArray<UPrimitiveComponent*>& OutComponents, const FName ComponentTag)
{


	if(UBlueprintGeneratedClass* GeneratedClass = Cast<UBlueprintGeneratedClass>(Blueprint->GeneratedClass))
	{
		// 创建临时Actor实例
		FActorSpawnParameters SpawnParams;
		SpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		AActor* TempActor = GEditor->GetEditorWorldContext().World()->SpawnActor<AActor>(GeneratedClass, SpawnParams);
		TempActor->Tags.AddUnique("PythonTemp");
		// 获取所有实例化后的组件
		TArray<UActorComponent*> InstanceComponents;
		TempActor->GetComponents(InstanceComponents);

		for(UActorComponent* Component : InstanceComponents)
		{
			if(UPrimitiveComponent* PrimComp = Cast<UPrimitiveComponent>(Component))
			{
				if(PrimComp->ComponentHasTag(ComponentTag))
				{
					OutComponents.Emplace(PrimComp);
				}
			}
		}

		// 销毁临时Actor（根据实际需求决定是否立即销毁）
		//TempActor->Destroy();
	}


	// if(UBlueprintGeneratedClass* GeneratedClass = Cast<UBlueprintGeneratedClass>(Blueprint->GeneratedClass))
	// {
	// 	TArray<USCS_Node*> AllNodes = GeneratedClass->SimpleConstructionScript->GetAllNodes();
	// 	for (USCS_Node* Node : AllNodes)
	// 	{
	// 		UActorComponent* ComponentTemplate = Node->GetActualComponentTemplate(GeneratedClass);
	// 		if(UStaticMeshComponent* MeshComponent = Cast<UStaticMeshComponent>(ComponentTemplate))
	// 		{
	// 			if(MeshComponent->ComponentHasTag(ComponentTag))
	// 			{
	// 				UE_LOG(LogTemp, Log, TEXT("DX>>> 组件名:%s :相对位置%s"),*MeshComponent->GetName(),*MeshComponent->GetRelativeLocation().ToString());
	// 				OutComponents.Emplace(MeshComponent);
	// 			}
	// 		}
	// 	}
	// }
	
}