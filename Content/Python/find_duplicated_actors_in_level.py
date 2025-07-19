import unreal

EditorActorSubsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = EditorActorSubsystem.get_all_level_actors()

actors_per_asset_group = []
for actor in actors:
    #只处理静态网格体Actor
    if not isinstance(actor, unreal.StaticMeshActor):
        continue

    found = False
    # 按静态网格资源分组
    for group in actors_per_asset_group:
        if actor.static_mesh_component.static_mesh.get_full_name() == \
            group[0].static_mesh_component.static_mesh.get_full_name():
            group.append(actor)
            found = True
            break

    if not found:
        actors_per_asset_group.append([actor])

# 只保留引用同一资源且数量大于等于2的分组
actors_per_asset_group = [a for a in actors_per_asset_group if len(a) >=2]

# 查找位置相近的 Actor
duplicates_groups = []
for actors_group in actors_per_asset_group:
    matched_indexes = []

    # 倒序遍历，查找位置相近的 Actor
    for i in range(len(actors_group) - 1,-1,-1):
        if i in matched_indexes:
            continue

        current = actors_group[i]
        nearby_actors = [current]
        actors_group.pop(i)

        for j in range(len(actors_group)-1, -1, -1):
            if j in matched_indexes:
                continue

            comparing_to = actors_group[j]
            # 判断 Transform 是否近似相等
            if current.get_actor_transform().is_near_equal(comparing_to.get_actor_transform(),0.1):
                nearby_actors.append(comparing_to)
                matched_indexes.append(j)
        
        if len(nearby_actors) > 1:
            duplicates_groups.append(nearby_actors)

#输出结果
for actor_group in duplicates_groups:
    for actor in actor_group:
        print(f"{actor.get_full_name()} | {actor.static_mesh_component.static_mesh.get_full_name()} | {actor.get_actor_transform().translation}")

    print(20* "-")